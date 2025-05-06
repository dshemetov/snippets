from hashlib import sha256
from pathlib import Path


def dedup_radian_history_file(path, output_path=None, keep_latest=True):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    current_block = []
    in_entry = False

    for line in lines:
        if line.startswith("# time:"):
            if current_block:
                entries.append(current_block)
                current_block = []
            in_entry = True
        if in_entry:
            current_block.append(line)

    if current_block:
        entries.append(current_block)

    # Dedup by hash of the command text (ignoring metadata)
    seen = {}
    deduped_entries = []

    for entry in reversed(entries) if keep_latest else entries:
        command_lines = [l[1:] for l in entry if l.startswith("+")]
        command_text = "".join(command_lines).strip()
        hashval = sha256(command_text.encode()).hexdigest()

        if hashval not in seen:
            seen[hashval] = True
            deduped_entries.append(entry)

    # Preserve original order if keep_latest
    if keep_latest:
        deduped_entries.reverse()

    # Output result
    output_path = output_path or path
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in deduped_entries:
            f.writelines(entry)

    print(f"Wrote deduplicated history to {output_path}")


# Backup original file
def backup_file(path):
    # Determine backup path
    backup_path = path.with_suffix(".bak")
    if backup_path.exists():
        i = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f".bak{i}")
            i += 1

    # Create backup
    with open(path, "r", encoding="utf-8") as original:
        with open(backup_path, "w", encoding="utf-8") as backup:
            backup.writelines(original.readlines())


if __name__ == "__main__":
    backup_file(Path.home() / ".radian_history")
    dedup_radian_history_file(Path.home() / ".radian_history", keep_latest=True)
