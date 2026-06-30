FROM python:3.12

LABEL authors="xuwenqing" maintainer="xwq<wenqing814@outlook.com>"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./

#缓存挂载,多次构建时,uv 的下载缓存会被复用,加速构建,临时挂载，只在 RUN 命令执行期间存在
# 将宿主机/构建上下文中的 uv.lock 文件挂载到容器内
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project

COPY . .

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]