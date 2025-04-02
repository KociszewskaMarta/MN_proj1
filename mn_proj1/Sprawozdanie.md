Marta Kociszewska 198143   
### **1. Wstęp**  
  
Wskaźnik **MACD** (skrót od ang. _Moving Average Convergence/Divergence_), czyli konwergencja i dywergencja średnich kroczących, jest jednym z najczęściej stosowanych narzędzi analizy technicznej na rynkach finansowych. Jego głównym celem jest identyfikacja trendów rynkowych oraz generowanie sygnałów kupna i sprzedaży poprzez analizę relacji między dwiema średnimi kroczącymi cen zamknięcia.

MACD opiera się na różnicy pomiędzy krótkoterminową i długoterminową wykładniczą średnią kroczącą (EMA). Standardowe ustawienia obejmują **12-okresową EMA** oraz **26-okresową EMA**, których różnica tworzy tzw. **linię MACD**. Dodatkowo obliczana jest **9-okresowa EMA linii MACD**, zwana **linią sygnałową**, która pomaga w identyfikacji punktów zwrotnych na rynku.

Główną zaletą MACD jest jego zdolność do wykrywania momentów, w których dynamika cen zyskuje na sile lub słabnie, co może sygnalizować odwrócenie trendu. Analiza przecięć linii MACD i linii sygnałowej, a także histogramu MACD, umożliwia określenie potencjalnych punktów wejścia i wyjścia z rynku. Wskaźnik ten jest powszechnie stosowany zarówno w analizie akcji, walut, surowców, jak i kryptowalut, dzięki swojej uniwersalności i łatwości interpretacji.
  
----  
### **2. Dane testowe**  
  
Dane, które zostały wykorzystane w analizie, pochodzą z historycznych notowań indeksu WIG20, obejmujących około 1100 notowań w okresie od 2020-10-01 do 2025-03-12. Indeks WIG20 jest jednym z najważniejszych wskaźników giełdowych w Polsce, reprezentującym 20 największych i najbardziej płynnych spółek na warszawskiej giełdzie. Dane obejmują zmiany cen zamknięcia, wartości indeksu oraz inne istotne parametry, takie jak wolumen obrotu i zmienność rynkowa, które mogą być wykorzystane do analizy trendów rynkowych, badania zmienności, czy też testowania różnych strategii inwestycyjnych.   
  
Obliczenia będą oparte na datach i cenach zamknięcia.  
  
Tabela zawiera przykładowe dane notowań indeksu WIG20.  

| Data       | Otwarcie | Najwyzszy | Najnizszy | Zamkniecie | Wolumen  |
| ---------- | -------- | --------- | --------- | ---------- | -------- |
| 2020-10-01 | 1719.55  | 1723.85   | 1697.54   | 1694.18    | 22310007 |
| 2020-10-02 | 1690.04  | 1704.58   | 1675.2    | 1697.39    | 18298699 |
  
Dane zostały pobrane z serwisu *stooq.pl*, który oferuje darmowy dostęp do historycznych notowań giełdowych, indeksów, walut, czy towarów.  
  
Wykres 2.1 przedstawia zmiany cen zamknięcia dla wskaźnika WIG20 w okresie od 2020-10-01 do 2025-03-12.  
  
![[closing_prices.png]]
<small>Wykres 2.1 Wykres giełdowy WIG20</small>  

W analizowanym okresie indeks WIG20 wykazywał zmienność, z okresami zarówno wzrostów, jak i spadków. Najniższy poziom odnotowano w 2022 roku, podczas gdy lata 2021,2023 i 2024 przyniosły znaczące wzrosty. Dane z początku 2025 roku wskazują na dalszą zmienność. 

Spadek WIG20 w 2022 roku był głównie wynikiem trudnej sytuacji geopolitycznej związanej z wojną na Ukrainie, wzrostem inflacji i niepewności gospodarczej. Natomiast wzrost w 2021, 2023 i 2024 roku wynikał z odbudowy po pandemii, stabilizacji gospodarczej, wzrostu inwestycji oraz adaptacji do wyzwań inflacyjnych i geopolitycznych, co pozwoliło na długoterminowy wzrost wartości indeksu.

----
### **3. Konstrukcja i analiza wskaźnika MACD**  
  
Wskaźnik MACD obliczany przy użyciu wykładniczej średniej kroczącej **EMA** (skrót od ang. *Exponentail Moving Avarage*) obliczanej według wzoru:  
$$ EMA_N(i) = \alpha \cdot x_i + (1-\alpha) \cdot EMA_N(i - 1)  
\tag{1}$$  
gdzie:   
- $x_i$ - cena zamknięcia w $i$-tym okresie  
- $N$ - liczba okresów  
- $\alpha$ - współczynnik wygładzający: $\alpha = \frac{2}{N+1}$  
  
Równanie $(1)$ można przekształcić do postaci jawnej:  
$$  
EMA_N(i) =   
\frac  
{x_1 + (1-\alpha)x_{i-1} + (1-\alpha)^2 x_{i-2} + ... + (1-\alpha)^N x_{i-N}}  
{1+ (1 - \alpha) + (1 - \alpha)^2 + ... + (1 - \alpha)^N}  
\tag{2}  
$$  
Jest to forma średniej ważonej, w której wagi dla wcześniejszych cen zmniejszają się w sposób wykładniczy. Tego rodzaju średnia szybciej reaguje na zmiany cen aktywa, uwzględniając jednocześnie wszystkie wcześniejsze ceny, przy jednoczesnym stopniowym osłabianiu ich wpływu.  
  
Z obu przedstawionych równań wynika, że wartość **EMA** dla $i$-tego okresu zależy zarówno od bieżącej ceny zamknięcia $x_i$ jak i od wszystkich wcześniejszych cen. W obliczeniach **EMA** pojawia się problem ustalenia wartości początkowej. Z równania (2) wynika, że 26-dniową EMA można obliczyć już po drugiej cenie, co nie odpowiada intuicyjnemu rozumieniu średniej 26-dniowej, ponieważ pomija pierwsze dni. Przy założeniu, że $EMA_N(0)=x_0$ obliczenia mogą prowadzić do oscylacji, które źle odwzorowują zmienność cen. Aby poprawić dokładność początkowych wartości, obliczenia zaczyna się od $i=N+1$, gdzie wartość $EMA_N(N)$ to średnia z pierwszych $N$ cen. Należy zaznaczyć, że bez względu na metodę, wyniki **EMA** dla kolejnych okresów będą zbieżne, a stabilizacja następuje zazwyczaj po $N$-tym, choć preferowane jest $2N$-tym okresie.  
##### **Krzywa MACD**  
Krzywa **MACD** wyznaczana jest przez różnicę między szybką a wolną średnią kroczącą. W popularnym podejściu średnie przyjmują wartość:  
- $EMA_{12}$ - 12-okresowa wykładnicza średnia krocząca,  
- $EMA{26}$ - 26-okresowa wykładnicza średnia krocząca.  
  
Wówczas krzywą **MACD** można obliczyć według wzoru:  
$$  
MACD = EMA_{12} - EMA_{26}  
\tag{3}  
$$  
  
##### **Krzywa SIGNAL**  
W wyżej wspomnianym podejściu krzywa **SIGNAL** wyznaczana jest jako 9-okresowa wykładnicza średnia krocząca obliczana na podstawie wartości **MACD**.  
  
Krzywą można obliczyć według wzoru:  
$$  
SIGNAL = EMA_9 (MACD)  
\tag{4}  
$$  
  
Wskaźnik został zaimplementowany w języku Python z wykorzystaniem bibliotek pandas oraz matplotlib. Wykorzystano wzór (1) do obliczenia *EMA*

----
### **4. Interpretacja wskaźnika MACD**  
  
Wskaźnik **MACD** jest używany do identyfikacji trendów rynkowych, sygnałów kupna i sprzedaży oraz do analizy zmienności cen. Podstawowe zasady interpretacji wskaźnika **MACD**:  
- **Krzywa MACD** powyżej zera - sygnał wzrostowy, poniżej zera - sygnał spadkowy,  
- **Krzywa SIGNAL** przecina **MACD** od dołu - sygnał kupna, od góry - sygnał sprzedaży,  
- **Krzywa MACD** i **SIGNAL** powyżej zera - sygnał wzrostowy, poniżej zera - sygnał spadkowy,  
  
Warto zaznaczyć, że wskaźnik **MACD** nie jest wskaźnikiem samym w sobie, ale jedynie narzędziem, które należy interpretować w kontekście innych wskaźników i analizy rynkowej.   
Wskaźnik **MACD** jest jednym z wielu narzędzi analizy technicznej, które mogą być wykorzystane do analizy rynku finansowego.  
  
Wykres 4.1 przedstawia wartości **MACD** oraz **SIGNAL** dla indeksu WIG20 w okresie od 2020-10-01 do 2025-03-12.   
![[macd_and_signal.png]]
<small>Wykres 4.1. Wykres MACD przy użyciu zaimplementowanych funkcji</small>  

Aby zweryfikować poprawność implementacji wskaźnika MACD, do sprawozdania dołączono również wykres 4.2 przedstawiający wykres MACD obliczony przy użyciu oprogramowania *MATLAB*, korzystając z funkcji `macd` pochodzącej z pakietu *Financial Toolbox*. Dzięki temu możliwe jest porównanie wyników obu metod i ocena zgodności uzyskanych rezultatów.

Wykres 4.2 przedstawia wartości **MACD** oraz **SIGNAL**  dla indeksu WIG20 w okresie od 2020-10-01 do 2025-03-12 obliczone przy użyciu *MATLAB* i funkcji `macd`.

![[macd_plot_by_matlab.png]]
<small>Wykres 4.2. Wykres MACD przy użyciu oprogramowania MATLAB</small>

Histogram **MACD** to graficzna reprezentacja różnicy między linią MACD a linią sygnałową. Pokazuje on dynamikę zmian siły trendu oraz momenty, w których może dojść do odwrócenia kierunku cen. Histogram jest obliczany jako:
$$ \text{Histogram MACD = MACD line - SIGNAL line}$$
Gdy wartości histogramu są dodatnie, oznacza to, że linia MACD znajduje się powyżej linii sygnałowej, co może wskazywać na przewagę trendu wzrostowego. Natomiast wartości ujemne sugerują, że linia MACD jest poniżej linii sygnałowej, co może oznaczać trend spadkowy. Wzrosty i spadki słupków histogramu pozwalają również ocenić siłę zmian cen oraz potencjalne punkty odwrócenia trendu.

Wykres 4.3 przedstawia histogram wartości **MACD** oraz **SIGNAL** w okresie od 2020-10-01 do 2020-12-31.  
![[histogram.png]]
<small>Wykres 4.3. Histogram</small>  

Wskaźnik **MACD** oraz jego linia sygnałowa są często analizowane poprzez ich wzajemne przecięcia, które dostarczają istotnych informacji na temat możliwych zmian trendu. Analiza tych przecięć pomaga w identyfikacji momentów wejścia i wyjścia z rynku oraz w ocenie siły trendu.

Wykres 4.4 przedstawia wartości **MACD** oraz **SIGNAL** w okresie od 2020-10-01 do 2020-12-31, wraz z zaznaczonymi momentami, w których krzywa **SIGNAL** przecina krzywą **MACD**.  

![[macd_signal_cross_points.png]]
<small>Wykres 4.4 Wykres MACD i SIGNAL z zaznaczonymi punktami przecięcia</small>  

Gdy **MACD** przecina linię **SIGNAL** od dołu, jest to uznawane za **sygnał kupna**, sugerujący, że trend wzrostowy może nabierać na sile. Natomiast gdy **MACD** przecina linię **SIGNAL** od góry, oznacza to **sygnał sprzedaży**, co może wskazywać na osłabienie trendu wzrostowego i potencjalny ruch spadkowy.

Wykres 4.5 przedstawia wartości **MACD** oraz **SIGNAL** w okresie od 2020-10-01 do 2020-12-31, wraz z zaznaczonymi sygnałami kupna i sprzedaży.  

Sygnał kupna został oznaczony kolorem zielonym, sygnał sprzedaży - kolorem czerwonym.  

![[macd_signal_buy_sell_points.png]]
<small>Wykres 4.5 Wykres MACD i SIGNAL z zaznaczonymi sygnałami kupna i sprzedaży</small>  
  
### **5. Analiza przykładowych transakcji i prezentacja problemów ze wskaźnikiem MACD**  

#### **Analiza przykładowych transakcji**

Na podstawie wykresu 4.5 **MACD i SIGNAL** dla WIG20, można przeprowadzić analizę kilka okresów, w których **MACD** sygnalizował momenty kupna i sprzedaży.

Wykres 5.1 przedstawia sygnał **MACD** oraz linię sygnału (**SIGNAL**) dla okresu od października 2020 roku do stycznia 2021 roku. 
Pod koniec października na wykresie widzimy pierwszy sygnał sprzedaży. Ten sygnał zbiega się z początkiem trendu spadkowego, co potwierdza spadek wartości **MACD** poniżej linii **SIGNAL**. W połowie listopada pojawia się sygnał kupna, który przewiduje tren wzrostowy. Później pojawia się kolejny sygnał sprzedaży, a pod koniec grudnia pojawia się sygnał kupna. Następnie pojawia się sygnał sprzedaży, który zapowiada korektę trendu. Pod koniec stycznia ponownie pojawia się kolejny sygnał kupna

![[macd_signal_buy_sell_points_for__2020-10-01_2021-01-31.png]]
<small>Wykres 5.1 Wykres MACD i SIGNAL dla okresu 10.2020-01.2021</small>   

**Analiza transakcji:**
1. **Sygnał sprzedaży:** (1556,14)
2. **Sygnał kupna:** (1799,02)
3. **Sygnał sprzedaży:** (1820,85)
4. **Sygnał kupna:** (2004,41)
5. **Sygnał sprzedaży:** (2074,11)
6. **Sygnał kupna:** (1986,09)

**Obliczenia zysków i strat:**
1. **Transakcja 1 (kupno-sprzedaż):** 1799,02 - 1556,14 = 242,88 (zysk)
2. **Transakcja 2 (sprzedaż-kupno):** 1820,85 - 1799,02 = 21,83 (zysk)
3. **Transakcja 3 (kupno-sprzedaż):** 2004,41 - 1820,85 = 183,56 (zysk)
4. **Transakcja 4 (sprzedaż-kupno):** 2074,11 - 2004,41 = 69,7 (zysk)
5. **Transakcja 5 (kupno-sprzedaż):** 1986,09 - 2074,11 = -88,02 (strata)

**Podsumowanie:**
- **Łączny wynik:** 242,88 + 21,83 + 183,56 + 69,7 - 88,02 = 429,95

Wykres 5.2 przedstawia sygnał **MACD** oraz linię sygnału (**SIGNAL**) dla okresu od czerwca 2022 roku do września 2022 roku. 
Pierwszy sygnał kupna pojawił się na początku czerwca, po czym nastąpił wzrost wartości **MACD**, co wskazywało na trend wzrostowy. Następnie w okolicach początku lipca pojawił się sygnał sprzedaży, po którym rzeczywiście nastąpił trend spadkowy – **MACD** opadał poniżej linii **SIGNAL**. Pod koniec lipca wystąpił kolejny sygnał kupna. Pod koniec sierpnia pojawiło się kilka sygnałów kupna i sprzedaży w krótkim odstępie czasu, co może wskazywać na okres konsolidacji, w którym brak było wyraźnego trendu. Natomiast ostatni sygnał kupna w sierpniu wyraźnie zapoczątkował silny trend wzrostowy, co pokazuje, że wskaźnik **MACD** w tym przypadku skutecznie zidentyfikował punkt zwrotny na rynku i wyznaczył odbicie ceny.

![[macd_signal_buy_sell_points_for__2022-06-01_2022-09-30.png]]
<small>Wykres 5.2 Wykres MACD i SIGNAL dla okresu 06.2022-09.2022</small>   

**Analiza transakcji:**
1. **Sygnał kupna:** (1822,57)
2. **Sygnał sprzedaży:** (1644,46)
3. **Sygnał kupna:** (1654,7)
4. **Sygnał sprzedaży:** (1684,14)
5. **Sygnał kupna:** (1640,02)
6. **Sygnał sprzedaży:** (1620,63)
7. **Sygnał kupna:** (1535,11)

**Obliczenia zysków i strat:**
1. **Transakcja 1 (kupno-sprzedaż):** 1644,46 - 1822,57 = -178,11 (strata)
2. **Transakcja 2 (kupno-sprzedaż):** 1684,14 - 1654,7 = 29,44 (zysk)
3. **Transakcja 3 (kupno-sprzedaż):** 1620,63 - 1640,02 = -19,39 (strata)
4. **Transakcja 4 (kupno-sprzedaż):** 1535,11 - 1620,63 = -85,52 (strata)

**Podsumowanie:**
- **Łączny wynik:** -178,11 + 29,44 - 19,39 - 85,52 = -253,58
#### **Wnioski**
Wyniki analizy pokazują, że skuteczność MACD w generowaniu zysków jest zmienna i zależy od konkretnego okresu rynkowego. W niektórych okresach, jak ten z 2020-10 do 2021-01, MACD generował sygnały, które mogły przynieść zysk. W innych okresach, jak ten z 2022-06 do 2022-09, sygnały MACD prowadziły do strat. Analiza potwierdza, że MACD, podobnie jak inne wskaźniki analizy technicznej, nie gwarantuje zysków. 

#### **Problemy ze wskaźnikiem MACD**

Podczas używania wskaźnika MACD (*Moving Average Convergence Divergence*) mogą pojawić się różne problemy związane z interpretacją sygnałów i jego ograniczeniami. Są to między innymi:
#### **1. Fałszywe sygnały**

- **MACD** czasem generuje sygnały kupna lub sprzedaży, które okazują się nietrafione, szczególnie na rynku o niskiej zmienności lub podczas konsolidacji.
- Przykład: Wskaźnik może zasugerować sygnał kupna (przecięcie linii MACD od dołu przez linię sygnału), ale cena aktywa nie rośnie, co prowadzi do strat.

Wykres 5.3 przedstawia sygnał **MACD** oraz linię sygnału (**SIGNAL**) dla okresu od lutego 2021 roku do połowy marca 2021 roku. W analizowanym przedziale czasowym można zaobserwować brak wyraźnego trendu, co prowadzi do tzw. konsolidacji rynkowej. W efekcie przecięcia linii **MACD** i **SIGNAL** występują wielokrotnie w krótkich odstępach czasu, co generuje liczne sygnały kupna i sprzedaży. Niestety, żaden z tych sygnałów nie jest poparty dynamiczną zmianą cen, co sprawia, że mają one charakter fałszywy.

![[macd_signal_buy_sell_points_for__2021-02-01_2021-03-15.png]]
<small>Wykres 5.3 Wykres MACD i SIGNAL dla okresu 02.2021-03.2021</small>   

Widać kilka miejsc, gdzie pojawiają się sygnały kupna (zielone trójkąty) i sprzedaży (czerwone trójkąty), ale zmiany te nie prowadzą do silnych trendów.

- Sygnał kupna pojawia się, po czym kurs nie rośnie znacząco i szybko generowany jest sygnał sprzedaży.
- Podobnie sygnały sprzedaży nie są potwierdzone dalszym spadkiem, a raczej niewielkimi wahaniami, co sprawia, że sygnał traci na wartości.
	
To typowy przykład **fałszywego sygnału w konsolidacji**, gdzie linie **MACD** i **SIGNAL** często się przecinają, ale brak wyraźnego trendu utrudnia skuteczne podejmowanie decyzji.

Wykres 5.4 przedstawia sygnał **MACD** oraz linię sygnału (**SIGNAL**) dla okresu od lipca 2023 roku do sierpnia 2023 roku. Ten okres również charakteryzuje się  niską zmiennością, co ponownie powoduje powstawanie fałszywych sygnałów.

![[macd_signal_buy_sell_points_for__2023-07-01_2023-08-31.png]]
<small>Wykres 5.4 Wykres MACD i SIGNAL dla okresu 07.2023-08.2023</small>  

Podobnie jak w poprzednim przykładzie, linie **MACD** i **SIGNAL** przecinają się kilka razy, co generuje sygnały kupna i sprzedaży w krótkim odstępie czasu.

- Inwestor, który reagowałby na te sygnały, mógłby szybko kupić i sprzedać, nie osiągając zysku, ponieważ po każdej transakcji kurs powraca do poziomu wyjściowego lub zmienia się minimalnie.
- Fałszywe sygnały są widoczne szczególnie w miejscach, gdzie nie ma wyraźnego kierunku – rynek porusza się w trendzie bocznym (konsolidacja).

**Dlaczego pojawiają się fałszywe sygnały?**

Fałszywe sygnały są powszechne podczas konsolidacji lub niskiej zmienności, ponieważ MACD reaguje na drobne zmiany w cenach, co prowadzi do wielokrotnych przecięć linii MACD i Signal. To z kolei generuje sygnały kupna i sprzedaży, które nie są poparte rzeczywistymi zmianami trendu.

**Jak ograniczyć wpływ fałszywych sygnałów?**

1. **Filtracja sygnałów**: Stosowanie dodatkowych wskaźników.
2. **Wydłużenie okresu MACD**: Zmiana parametrów MACD (np. 9, 21, 50) może zmniejszyć liczbę fałszywych sygnałów, choć kosztem opóźnień.
3. **Analiza trendu**: Unikanie sygnałów MACD w okresach konsolidacji i korzystanie z niego głównie podczas wyraźnych trendów wzrostowych lub spadkowych.

#### **2. Opóźnienie sygnałów**

- **MACD** opiera się na średnich kroczących, które są wskaźnikami opóźnionymi. Oznacza to, że sygnał może pojawić się dopiero po rozpoczęciu nowego trendu, co zmniejsza potencjalne zyski.
- Przykład: Jeśli rynek szybko zmienia kierunek, wskaźnik może reagować za późno, gdy znacząca część ruchu cenowego już się dokonała.

Wykres 5.5 przedstawia sygnał **MACD** oraz linię sygnału (**SIGNAL**) dla okresu od 2021-01-15 do 2021-02-04. Analiza tego przedziału czasowego uwidacznia istotną cechę wskaźnika MACD, jaką jest opóźnienie sygnału w stosunku do rzeczywistych zmian trendu. W omawianym okresie można zauważyć, że sygnał sprzedaży generowane przez przecięcie linii **MACD** i **SIGNAL** pojawiają się z pewnym opóźnieniem w stosunku do momentu faktycznej zmiany kierunku ruchu cen na rynku. 

![[macd_signal_buy_sell_points_for__2021-01-15_2021-02-04.png]]
<small>Wykres 5.5 Wykres MACD i SIGNAL dla okresu 01.2021 - 02.2021</small>  

**MACD** zarekomendował kupno akcji po cenie 1986.06 zł oraz sprzedaż po cenie 1967.22 zł prowadząc do straty na poziomie 18.84 zł. Nie jest to duża strata, jednak stanowi przykład na to, że **MACD** nie nie zawsze działa niezawodnie. 

**Dlaczego pojawia się opóźnienie sygnałów?**

Opóźnienie to wynika z natury MACD, który bazuje na średnich kroczących (domyślnie 12-dniowa i 26-dniowa). Średnie te są opóźnionymi wskaźnikami, więc dopiero po kilku dniach wyraźnego ruchu generują sygnał.

**Jak ograniczyć wpływ opóźnionych sygnałów?**

1. **Zastosowanie filtrów trendów**: Połączenie MACD z innymi wskaźnikami, może pomóc wyeliminować opóźnione sygnały w okresach konsolidacji. 
2. **Zastosowanie krótszych okresów dla średnich**: Użycie szybszych parametrów dla średnich wykładniczych (np. 6, 13, 26) może zmniejszyć opóźnienie sygnałów generowanych przez MACD, ale może również zwiększyć liczbę fałszywych sygnałów. Ważne jest, aby balansować szybkość sygnałów z ich wiarygodnością.
3. **Wykorzystanie analizy wolumenu**: Opóźnione sygnały mogą być bardziej wiarygodne, jeśli pojawiają się z dużym wolumenem obrotu. Obserwowanie zmian w wolumenie obrotu może pomóc ocenić siłę sygnału MACD, zmniejszając wpływ opóźnionych i słabszych sygnałów.

### **5. Podsumowanie**  

Analiza badanego wskaźnika wykazała, że jego skuteczność nie jest jednoznaczna – w zależności od warunków i okoliczności rynkowych przynosił zarówno zyski, jak i straty. Oznacza to, że nie można go traktować jako niezawodnego narzędzia prognostycznego, a jego interpretacja powinna uwzględniać dodatkowe czynniki wpływające na wynik końcowy.

Potencjalna opłacalność – **MACD** może dostarczać sygnały pozwalające na osiąganie zysków, zwłaszcza gdy jest stosowany w silnych trendach. Przecięcie linii sygnałowej może wskazywać momenty wejścia i wyjścia z rynku. Gdy **WIG20** znajduje się w wyraźnym trendzie wzrostowym lub spadkowym – wtedy sygnały przecięcia linii **MACD** i sygnałowej mogą wskazywać dobre momenty kupna/sprzedaży. W okresach silnej zmienności, gdy **MACD** wyraźnie oddziela trend wzrostowy od spadkowego.

Jednak w okresach konsolidacji, gdy indeks **WIG20** porusza się w wąskim zakresie – wtedy **MACD** może generować fałszywe sygnały kupna i sprzedaży, co może prowadzić do strat. Ponieważ MACD bazuje na średnich kroczących, jego sygnały są często opóźnione w stosunku do rzeczywistych zmian cen. Może to skutkować wejściem w pozycję zbyt późno, gdy większa część ruchu już się wydarzyła.

Analiza wskaźnika MACD w kontekście WIG20 wskazuje, że jest on bardziej przydatny w inwestycjach długoterminowych niż krótkoterminowych. Jego sygnały lepiej odzwierciedlają zmiany w długofalowych trendach, co pozwala na identyfikację korzystnych momentów wejścia i wyjścia z rynku. W krótkim terminie MACD może generować fałszywe sygnały, szczególnie w okresach konsolidacji, co zwiększa ryzyko nietrafionych decyzji inwestycyjnych. Dlatego stosowanie go jako narzędzia do strategii długoterminowych wydaje się bardziej opłacalne.

Podsumowując, MACD może być skutecznym narzędziem, ale jego sygnały powinny być zawsze weryfikowane za pomocą dodatkowych metod analizy, aby zminimalizować ryzyko strat i zwiększyć szanse na zysk. Jego skuteczność nie jest stuprocentowa, a stosowanie go bez dodatkowej analizy może prowadzić do strat. Wymaga ostrożnego stosowania i uwzględnienia kontekstu rynkowego. Inwestorzy powinni łączyć analizę techniczną z fundamentalną i stosować zasady zarządzania ryzykiem, aby zwiększyć szanse na sukces.

