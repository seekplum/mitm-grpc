define PRINT_HELP_PYSCRIPT
import re, sys

print("make option")
print("  --option:")
for line in sys.stdin:
    match = re.match(r'^([0-9a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print("    {:<20}{}".format(target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help: ## 帮助信息
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-pyc: ## 清理 Python 运行文件
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-grpc: ## 清理自动生成的grpc文件
	rm -f app/protos/hello_pb2.py
	rm -f app/protos/hello_pb2_grpc.py
	rm -f go-client/protos/hello.pb.go
	rm -f mygrpc/keys/key.pem
	rm -f mygrpc/keys/cert.pem
	rm -f mygrpc/keys/mitm.pem

clean-test: ## 清理测试文件
	rm -f .coverage
	rm -fr .pytest_cache

clean: clean-pyc clean-grpc clean-test ## 清理所有不该进代码库的文件
