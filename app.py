from flask import Flask
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# Setup OTel Metrics
exporter = OTLPMetricExporter(endpoint="otel-collector:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)
counter = meter.create_counter("flask_request_count", unit="1", description="Counts requests")

FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello():
    counter.add(1)
    return "Hello from OpenTelemetry - attempt 2!"

@app.route("/healthz")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
