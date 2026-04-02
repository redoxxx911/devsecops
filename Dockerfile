FROM python:3.11-slim

# Create a non-root user with a home directory (-m)
RUN groupadd -r appgroup && useradd -r -m -g appgroup appuser

# Set working directory and ownership
WORKDIR /app
RUN chown appuser:appgroup /app

# Switch to non-root user
USER appuser

# Copy requirements and install
COPY --chown=appuser:appgroup app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Ensure local bin is in PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy application code
COPY --chown=appuser:appgroup app/ .

# Expose port and run uvicorn
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
