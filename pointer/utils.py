def getTimeDiff(entry_time, exit_time):

    """
    [PT]

    Obter a diferença de tempo entre dois objetos datetime.

    @param entry_time(Time): O tempo de entrada.
    @param exit_time(Time): O tempo de saída.

    @return (int): A diferença de tempo em segundos
    
    [EN]

    Get the time difference between two datetime objects.


    @param entry_time(Time): The entry time.
    @param exit_time(Time): The exit time.

    @return (int): The time difference in seconds

    """
    return (exit_time - entry_time).total_seconds()