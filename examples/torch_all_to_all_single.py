"""Two-rank variable-split NCCL example visualized by the matching sviz trace.

Run on a machine with two CUDA GPUs:

    torchrun --standalone --nproc-per-node=2 \
        examples/torch_all_to_all_single.py
"""

from __future__ import annotations

import os

import torch
import torch.distributed as dist


def main() -> None:
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    dist.init_process_group(backend="nccl")

    try:
        rank = dist.get_rank()
        if dist.get_world_size() != 2:
            raise RuntimeError("this minimal example requires exactly two ranks")

        device = torch.device("cuda", local_rank)
        input_tensor = torch.arange(
            rank * 10, rank * 10 + 4, dtype=torch.int64, device=device
        )

        # A routing kernel would normally produce these device-resident counts.
        send_counts_gpu = torch.tensor(
            [1, 3] if rank == 0 else [2, 2],
            dtype=torch.int32,
            device=device,
        )
        recv_counts_gpu = torch.empty_like(send_counts_gpu)

        # Exchange one count per peer while all counts are still on the GPU.
        dist.all_to_all_single(recv_counts_gpu, send_counts_gpu)

        # all_to_all_single takes host split vectors. These D2H copies and list
        # materializations are therefore a host-visible synchronization point.
        input_split_sizes = send_counts_gpu.cpu().tolist()
        output_split_sizes = recv_counts_gpu.cpu().tolist()
        output_tensor = torch.empty(
            sum(output_split_sizes), dtype=input_tensor.dtype, device=device
        )

        # Variable splits use grouped peer Send/Recv operations in
        # ProcessGroupNCCL. Delaying wait() leaves room for independent work.
        work = dist.all_to_all_single(
            output_tensor,
            input_tensor,
            output_split_sizes=output_split_sizes,
            input_split_sizes=input_split_sizes,
            async_op=True,
        )
        independent = torch.arange(1024, dtype=torch.float32, device=device)
        independent.square_()
        work.wait()

        expected_values = (
            [0, 10, 11] if rank == 0 else [1, 2, 3, 12, 13]
        )
        expected = torch.tensor(
            expected_values,
            dtype=torch.int64,
            device=output_tensor.device,
        )
        torch.testing.assert_close(output_tensor, expected)
        print(
            f"rank {rank}: input={input_tensor.cpu().tolist()} "
            f"send_splits={input_split_sizes} "
            f"recv_splits={output_split_sizes} "
            f"output={output_tensor.cpu().tolist()}",
            flush=True,
        )
    finally:
        dist.destroy_process_group()


if __name__ == "__main__":
    main()
