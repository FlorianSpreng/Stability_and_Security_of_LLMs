from datetime import datetime

count = 0
time = 0
whole_count = 0
start_str = ""
ende_str = ""

with open("xmplrun.txt", encoding="utf-8") as run:
    for line in run:
        if "Ende: " in line:
            ende_str = line.split(": ")[1].strip()
        if "conversation safed in" in line:
            count += 1
        if "In Sekunden:" in line:
            time += float(line.split(": ")[1].strip())
        if "Start " in line:
            if start_str == "":
                start_str = line.split("Start ")[1].strip()
            whole_count += 1

whole_time = ((datetime.strptime(ende_str, "%Y-%m-%d %H:%M:%S.%f")
              - datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S.%f"))
              .total_seconds())

print(f"Von {whole_count} Dialogen sind {count} vollständig durchgelaufen."
      f"\nDabei wurde insgesamt {whole_time} Sekunden (also {((whole_time/60)/60):.2f} Stunden) benötigt,"
      f"\nFür die vollständigen läufe wurden durchschnittlich {time / count:.2f} (also"
      f" {(time / count) / 60:.2f} Minuten) sekunden/run benötigt.")
