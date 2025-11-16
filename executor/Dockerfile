FROM python:3.11-slim

WORKDIR /app

# Install data science packages
RUN pip install --no-cache-dir \
    pandas==2.1.4 \
    numpy==1.26.2 \
    scikit-learn==1.3.2 \
    matplotlib==3.8.2 \
    plotly==5.18.0 \
    seaborn==0.13.0 \
    scipy==1.11.4 \
    redis==5.0.1

COPY runner.py .

# Security: run as non-root
RUN useradd -m -u 1000 executor && chown -R executor:executor /app
USER executor

CMD ["python", "runner.py"]
