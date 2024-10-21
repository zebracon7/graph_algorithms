
all: 
	python3 main.py   

# Цель для запуска всех тестов
test:
	@echo "Запуск тестов..."
	coverage run -m unittest discover
	coverage report --include="s21_graph.py,s21_graph_algorithms.py"

# Цель для очистки временных файлов
clean:
	@rm -rf __pycache__ test_graph.dot test_graph.txt .coverage
