# ==========================================
# PADRÃO DE CRIAÇÃO: FACTORY METHOD
# ==========================================

# 1. Interface (Produto Abstrato)
class Metric:
    def to_json(self):
        raise NotImplementedError("Subclasses devem implementar to_json")

# 2. Produtos Concretos
class QuantitativeMetric(Metric):
    def __init__(self, name, value, data_type="integer"):
        self.name = name
        self.value = value
        self.data_type = data_type

    def to_json(self):
        return {
            "name": self.name,
            "type": self.data_type,
            "value": self.value
        }

class QualitativeMetric(Metric):
    def __init__(self, name, value, data_type="text/plain"):
        self.name = name
        self.value = value
        self.data_type = data_type

    def to_json(self):
        return {
            "name": self.name,
            "type": self.data_type,
            "value": self.value
        }

# 3. A Fábrica (Creator, que tambem atua como creatorConcrete neste caso (Parameterized Factory Method))
class MetricFactory:
    @staticmethod
    def create_metric(category, name, value, data_type=None):
        if category == "quant":
            dtype = data_type if data_type else "integer"
            return QuantitativeMetric(name, value, dtype)
        
        elif category == "qual":
            dtype = data_type if data_type else "text/plain"
            return QualitativeMetric(name, value, dtype)
            
        else:
            raise ValueError(f"Tipo de métrica desconhecido: {category}")
