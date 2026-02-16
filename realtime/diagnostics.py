# realtime/diagnostics.py
def run_diagnostics(events):
    diagnostics = {"total_events": len(events),
                   "alerts": sum(1 for e in events if e["alert"])}
    return diagnostics
