FROM python:3.10-slim
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./ /app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]