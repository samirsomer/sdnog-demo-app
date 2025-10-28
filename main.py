# ---------------------------------------------------------------------
# 1️⃣ Imports
# ---------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import random
import time
import logging

# --- OpenTelemetry Core ---
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

# --- Traces ---
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# --- Logs ---
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

# --- Metrics ---
from prometheus_fastapi_instrumentator import Instrumentator

# ---------------------------------------------------------------------
# 2️⃣ Resource Definition (used for all telemetry signals)
# ---------------------------------------------------------------------
resource = Resource.create({SERVICE_NAME: "demo-app"})

# ---------------------------------------------------------------------
# 3️⃣ OpenTelemetry TRACING Setup
# ---------------------------------------------------------------------
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)

# Export traces to the OpenTelemetry Collector (which sends to Jaeger)
otlp_trace_exporter = OTLPSpanExporter(
    endpoint="otel-collector:4317",  # gRPC endpoint inside Docker network
    insecure=True,
)
trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))

# ---------------------------------------------------------------------
# 4️⃣ OpenTelemetry LOGGING Setup
# ---------------------------------------------------------------------
# Create LoggerProvider and register globally
logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)

# Export logs via OTLP/HTTP to the Collector (→ Loki)
otlp_log_exporter = OTLPLogExporter(endpoint="http://otel-collector:4318/v1/logs")
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))

# Bridge Python logging → OpenTelemetry log pipeline
otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

# Standard Python logger setup
logger = logging.getLogger("demo-app")
logger.setLevel(logging.INFO)
logger.addHandler(otel_handler)


# Optional: also print logs to console with trace context
class TraceContextFormatter(logging.Formatter):
    """Add trace_id and span_id to console log lines."""

    def format(self, record):
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx.is_valid:
            record.trace_id = format(ctx.trace_id, "032x")
            record.span_id = format(ctx.span_id, "016x")
        else:
            record.trace_id = record.span_id = "N/A"
        return super().format(record)


console_handler = logging.StreamHandler()
console_handler.setFormatter(
    TraceContextFormatter(
        "%(asctime)s [%(levelname)s] trace_id=%(trace_id)s "
        "span_id=%(span_id)s %(message)s"
    )
)
logger.addHandler(console_handler)

# ---------------------------------------------------------------------
# 5️⃣ FastAPI App Definition
# ---------------------------------------------------------------------
app = FastAPI(title="FastAPI Observability Demo")


# ---------------------------------------------------------------------
# 6️⃣ Endpoints
# ---------------------------------------------------------------------
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello SdNOG 🚀!"}


@app.get("/random")
def get_random():
    value = random.randint(1, 100)
    logger.info(f"Generated random number: {value}")
    return {"random_number": value}


@app.get("/slow")
def slow_endpoint():
    logger.info("Simulating slow endpoint")
    time.sleep(1)
    logger.info("Slow endpoint completed")
    return {"message": "This endpoint was slow"}


@app.get("/error")
def error_endpoint():
    # logger.error("Simulated error triggered")
    return JSONResponse(status_code=500, content={"error": "Simulated error"})


# ---------------------------------------------------------------------
# 7️⃣ Instrumentation for FastAPI and Prometheus Metrics
# ---------------------------------------------------------------------
# Enable automatic tracing of FastAPI routes
FastAPIInstrumentor.instrument_app(app)

# Expose /metrics endpoint for Prometheus scraping
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)

# ---------------------------------------------------------------------
# ✅ End of main.py
# ---------------------------------------------------------------------
