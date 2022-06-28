1. Check the CPU info

	`lscpu | egrep 'Model name|Socket|Thread|NUMA|CPU\(s\)'`

2. Check memory

	`free -h`

3. Check disk

	`df -h`

4. Check GPU
	`lspci -v | egrep -i --color 'vga|3d|2d'`

	`nvidia-smi`

5. CUDA version
	`cat /usr/local/cuda/version.txt`