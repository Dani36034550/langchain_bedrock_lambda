FROM public.ecr.aws/lambda/python:3.12

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["lambda_function.lambda_handler"]

