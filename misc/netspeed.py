# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "speedtest",
# ]
# ///
import speedtest

s = speedtest.Speedtest()
s.get_servers()
s.get_best_server()
s.download()
s.upload()

with open("log.json", "a+") as f:
    f.write(s.results.json())
