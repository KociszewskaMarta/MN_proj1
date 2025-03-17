W przypadku **adresowania indeksowego** adres argumentu określony jest przez sumę zawartości pola adresowego rozkazu i rejestru indeksowego.

Pole adresowe to nie musi być konkretna liczba, może być wyrażeniem

![[Zrzut ekranu 2025-02-02 122411.png]]

> [!example] Przykład
```
add EAX, [EBX + 360]
```

> [!info] Symbolicznie
> $regs[R4] \leftarrow regs[R4]+ Mem [Regs[R1] + 360]$

> [!tip]
> W architekturze x86 rolę rejestru indeksowego może pełnić dowolny 32-bitowy rejestr ogólnego przeznaczenia: EAX, EBX, . . .


W przypadku szczególnym pole adresowe może być pominięte, co oznacza, że
adres argumentu określony jest wyłącznie przez zawartość rejestru indeksowego. W literaturze tego rodzaju adresowanie określane jest jako adresowanie za pomocą wskaźników

![[Zrzut ekranu 2025-02-02 122822.png]]
> [!example] Przykład
```
add EAX, [ESI]
```

> [!info] Symbolicznie
> $regs[R4] \leftarrow regs[R4]+ Mem [Regs[R1]]$
