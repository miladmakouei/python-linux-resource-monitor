
import psutil
from datetime import datetime


CPU_WARNING = 80
RAM_WARNING = 80
DISK_WARNING = 85


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_info():
    memory = psutil.virtual_memory()

    return {
        "total": memory.total,
        "used": memory.used,
        "available": memory.available,
        "percent": memory.percent
    }


def get_disk_info():
    disk = psutil.disk_usage("/")

    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    }


def format_bytes(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def show_top_processes():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_info"]
    ):
        try:
            info = process.info

            if info["memory_info"] is None:
                continue

            memory_usage = info["memory_info"].rss

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "memory": memory_usage
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(
        key=lambda item: item["memory"],
        reverse=True
    )

    print("\nTop 5 Memory-Consuming Processes")
    print("-" * 55)

    for process in processes[:5]:
        print(
            f"PID: {process['pid']:<8} "
            f"Name: {str(process['name'])[:20]:<20} "
            f"RAM: {format_bytes(process['memory'])}"
        )


def show_warnings(cpu, memory, disk):
    print("\nResource Warnings")
    print("-" * 55)

    warnings_found = False

    if cpu >= CPU_WARNING:
        print(f"[!] High CPU usage: {cpu}%")
        warnings_found = True

    if memory["percent"] >= RAM_WARNING:
        print(
            f"[!] High RAM usage: {memory['percent']}%"
        )
        warnings_found = True

    if disk["percent"] >= DISK_WARNING:
        print(
            f"[!] Low disk space: {disk['percent']}% used"
        )
        warnings_found = True

    if not warnings_found:
        print("[+] No resource warnings detected.")


def main():
    print("=" * 55)
    print("             LINUX SYSTEM RESOURCE MONITOR")
    print("=" * 55)

    print(
        f"\nReport Time: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    cpu = get_cpu_usage()
    memory = get_memory_info()
    disk = get_disk_info()

    print("\nCPU")
    print("-" * 55)
    print(f"Usage: {cpu}%")

    print("\nRAM")
    print("-" * 55)
    print(f"Total:     {format_bytes(memory['total'])}")
    print(f"Used:      {format_bytes(memory['used'])}")
    print(f"Available: {format_bytes(memory['available'])}")
    print(f"Usage:     {memory['percent']}%")

    print("\nDisk")
    print("-" * 55)
    print(f"Total: {format_bytes(disk['total'])}")
    print(f"Used:  {format_bytes(disk['used'])}")
    print(f"Free:  {format_bytes(disk['free'])}")
    print(f"Usage: {disk['percent']}%")

    show_top_processes()
    show_warnings(cpu, memory, disk)

    print("\n" + "=" * 55)
    print("Resource check completed.")
    print("=" * 55)


if __name__ == "__main__":
    main()
