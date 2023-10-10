import datetime
from abc import ABC, abstractmethod
from typing import List

from apis import DaySummaryApi


class DataIngestor(ABC):

    """
    Representa um ingestor de dados.

    A classe `DataIngestor` é uma classe base abstrata (ABC) que provê uma interface comum para ingestão de dados.
    Ela define a estrutura e comportamento básico de um ingestor.

    Args:
        writer: O objeto writer utilizado para escrever os dados.
        coins: Uma lista de strings representando as moedas a serem ingeridas.
        default_start_date: A data de inicio padrão para a ingestão.

    Atributos:
        coins (List[str]):  A lista de moedas a serem ingerida.
        default_start_date (datetime.date): A data de inicio padrão para a ingestão.
        writer: O objeto writer utilizado para escrever os dados.
        _checkpoint (datetime.date): A data de checkpoint para a ingestão de dados.

    Métodos:
        _checkpoint_filename: Retorna o nome do arquivo para o checkpoint.
        _write_checkpoint: Escreve a data de checkpoint no arquivo de checkpoint.
        _load_checkpoint: Carrega a data de checkpoint do arquivo de checkpoint.
        _get_checkpoint: Retorna a data de checkpoint ou a data de inicio padrão caso o checkpoint não esteja definido.
        _update_checkpoint: Atualiza a data de checkpoint e escreve para o arquivo de checkpoint.
        ingest: Método abstrato para a ingestão de dados.

    Exemplo:
        ```
        writer = DataWriter()
        coins = ['BTC', 'ETH']
        default_start_date = datetime.date(2022, 1, 1)
        ingestor = DataIngestor(writer, coins, default_start_date)
        ingestor.ingest()
        ```
    """

    def __init__(self, writer, coins:List[str], default_start_date: datetime.date) -> None:

        """
    Inicializa a instância do `DataIngestor`.

    O método `__init__` define os valores iniciais para a instância do `DataIngestor`.
    Atribui os valores fornecidos de `writer`, `coins`, e `default_start_date`  aos atributos correspondentes.
    Também carrega a data de checkpoint usando o métdodo `_load_checkpoint` e atribui ao atributo `_checkpoint`.

    Args:
        writer: O objeto writer utilizado para escrever os dados.
        coins (List[str]): Uma lista de strings representando as moedas a serem ingeridas.
        default_start_date (datetime.date): A data de inicio padrão para a ingestão.

    Retorna:
        None

    Exemplo:
        ```python
        writer = DataWriter()
        coins = ['BTC', 'ETH']
        default_start_date = datetime.date(2022, 1, 1)
        ingestor = DataIngestor(writer, coins, default_start_date)
        ```
    """

        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer
        self._checkpoint = self._load_checkpoint()

    @property
    def _checkpoint_filename(self) -> str:

        """
    Retorna o nome do arquivo de checkpoint.

    A propriedade `_checkpoint_filename` retorna uma string representando o nome do arquivo
    do checkpoint para a instâcia do `DataIngestor`.
    O nome do arquivo é gerado com base no nome da classe.

    Retorna:
        str: O nome do arquivo de checkpoint.

    Exemplo:
        ```python
        ingestor = DataIngestor()
        filename = ingestor._checkpoint_filename
        print(filename)  # Output: "DataIngestor.checkpoint"
        ```
    """
        return f'{self.__class__.__name__}.checkpoint'

    def _write_checkpoint(self):
        """
    Escreve a propriedade checkpoint no arquivo de checkpoint.

    O método `write_checkpoint` abre o arquivo indicado na propriedade _checkpoint_filename em
    modo write e escreve a string no arquivo.

    Retorna:
        None
    
    Exemplo:
        ```python
        ingestor = DataIngestor()
        ingestor._write_checkpoint()
        """
        with open(self._checkpoint_filename, "w") as f:
            f.write(f'{self._checkpoint}')

    def _load_checkpoint(self) -> datetime.date:
        """
    Obtém o valor do checkpoint atual como objeto datetime.date() e armazena na propriedade `._checkpoint`.

    O método `load_checkpoint` abre o arquivo indicado na propriedade _checkpoint_filename em modo
    de leitura, analisa o conteúdo com a função datetime.datetime.strptime() e o converte em um objeto datetime.date()

    Caso nenhum arquivo seja encontrao, o método falha e levanta uma exceção do tipo `FileNotFoundError`
    If no file is found, the method wil raise a `FileNotFoundError`

    Retorna:
        datetime.date(): O objeto datetime.date() do arquivo de checkpoint analisado.
    
    Exemplo:
        ```python
        ingestor = DataIngestor()
        ingestor._load_checkpoint
        ```
        """

        try:
            with open(self._checkpoint_filename, "r") as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return self.default_start_date

    def _get_checkpoint(self):
        """
    Retorna a data de checkpoint.

    O método `_get_checkpoint` retorna a data de checkpoint para a instãncia de `DataIngestor`.
    Se a data de checkpoint não está definida, retorna a data de inicio padrão.

    Retorna:
        datetime.date: A data de checkpoint.

    Exemplo:
        ```python
        ingestor = DataIngestor()
        checkpoint = ingestor._get_checkpoint()
        print(checkpoint)  # Output: A data de checkpoint ou a data de incio padrão.
        ```
        """
        return self._checkpoint or self.default_start_date

    def _update_checkpoint(self, value):
        """
    Atualiza a data de checkpoint

    O método `_update_checkpoint` atualiza a data de checkpoint para a instância de `DataIngestor`.
    Ele define o atributo `_checkpoint` com o valor fornecido `value`e escreve a data de checkpoint no
     arquivo de checkpoint usando o método `_write_checkpoint`.

    Argumentos:
        value: A nova data de checkpoint.

    Retorna:
        None

    Exemplo:
        ```python
        ingestor = DataIngestor()
        novo_checkpoint = datetime.date(2022, 1, 1)
        ingestor._update_checkpoint(novo_checkpoint)
        ```
    """

        self._checkpoint = value
        self._write_checkpoint()

    @abstractmethod
    def ingest(self) -> None:
        """
    Método abstrato para ingestão de dados.

    O método `ingest` é um método abstrato que precisa ser implementado por subclasses de `DataIngestor`.
    Ele define o comportamento para ingestão de dados.

    Argumentos:
        self

    Retorna:
        None

    Exemplo:
        Este método deve ser implementado em uma subclasse de `DataIngestor` para realizar a ingestão de fato.
    """
        pass


class DaySummaryIngestor(DataIngestor):
    """
    Representa um ingestor de dados da API day summary.

    A classe `DaySummaryIngestor` é uma subclasse de `DataIngestor` que se especializa em ingerir dados da API DaySummaryAPI.
    Ela sobrescreve o método `ingest` para realizar a ingestão de dados específica da API DaySummaryAPI.

    Métodos:
        ingest: Realiza a ingestão de dados na API DaySummaryApi.

    Exemplo:
        ```python
        ingestor = DaySummaryIngestor()
        ingestor.ingest()
        ```
    """

    def ingest(self) -> None:
        """
    Realiza a ingestão de dados para a API DaySummaryApi.

    O método `ingest` retorna a data de check;oint utilizando o método `_get_checkpoint`.
    Se a data de checkpoint é anterior a hoje, ele itera sobre as moedas e obtém os dados de sumário diário para cada moeda usando a API `DaySummaryApi`
    O dado então é escrito no writter correspondente utilizando o método write.
    Finalmente, a data de checkpoint é atualizada ao adicionar um dia utilizando o método `_update_checkpoint`.

    Argumentos:
        self

    Retorna:
        None

    Exemplo:
        ```python
        ingestor = DataIngestor()
        ingestor.ingest()
        ```
    """

        date = self._get_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date = date)
                self.writer(coin=coin, api= api.type).write(data)
            self._update_checkpoint(date + datetime.timedelta(days=1))


class DataTypeNotSupportedForIngestionException(Exception):
    """
    Exceção levantada para tipos de data não suportados durante a ingestão.

    A classe `DataTypeNotSupportedForIngestionException` é uma exceção 
    levantada quando um tipo de dados não suportado é encontrado durante a ingestão.
    
    Ela herdada classe `Exception` e sobrescreve o método `__init__` para definir o atributo
    `data` e gera uma mensagem indicando o time não suportado de dado.

    Args:
        data: O dado não suportado.

    Attributes:
        data: O dado não suportado.
        message: A mensagem de exceção.

    Example:
        ```python
        data = 123
        raise DataTypeNotSupportedForIngestionException(data)
        ```
    """

    def __init__(self, data):
        """
    Inicializa uma instância da DataTypeNotSupportedForIngestionException.

    O método `__init__` define o atributo `data` para o parâmetro provido de `data` e gera uma mensagem indicando que o tipo de dado não é suportado para ingestão.
    Ele chama o método `__init__` da classe pai `Exception` para inicializar a exceção.

    Argumentos:
        data: O dado não suportado.

    Atributos:
        data: O dado não suportado.
        message: A mensagem de exceção

    Exemplo:
        ```python
        data = 123
        raise DataTypeNotSupportedForIngestionException(data)
        ```
    """
        self.data = data
        self.message = f'Data type {type(data)} is not supported for ingestion'
        super().__init__(self.message)