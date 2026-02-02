from flask import Flask, jsonify, render_template
from capture import start_capture, packets, dns_leaks, lock ,ipv6_leaks

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/api/packets")
def get_packets():
    with lock:
        return jsonify(packets)

@app.route("/api/dnsleaks")
def get_dns_leaks():
    with lock:
        return jsonify({
            "leaks": dns_leaks,
            "count": len(dns_leaks)
        })
        
@app.route("/api/ipv6leaks")
def get_ipv6_leaks():
    with lock:
        return jsonify({"leaks": ipv6_leaks, "count": len(ipv6_leaks)})


if __name__ == "__main__":
    start_capture()
    app.run(host="0.0.0.0", port=5000, debug=False)
