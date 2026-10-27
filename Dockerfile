# =========================================================================
# Dockerfile for Java 21 Syntax Checker Web Application
# Targeted for Render Docker Web Service Deployment
# =========================================================================

FROM python:3.11-slim

# Prevent interactive prompts & buffer output
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Install build chain: GCC, Flex, GNU Bison, and standard libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    flex \
    bison \
    make \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy dependency specifications first for Docker layer caching
COPY requirements.txt .

# Install Python production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project source files
COPY . .

# Compile native Linux parser executable and shared object (.so)
RUN bison -v -d parser/java_parser.y --report-file=parser/java_parser.output -o parser/java_parser.tab.c && \
    flex -o lexer/lex.yy.c lexer/java_lexer.l && \
    gcc -O2 -Wall -Wno-unused-function -shared -fPIC -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.so && \
    gcc -O2 -Wall -Wno-unused-function -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck && \
    chmod +x javacheck

# Expose Render standard port
EXPOSE 5000

# Start production WSGI Gunicorn server binding to Render $PORT
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 60 backend.app:app"]
