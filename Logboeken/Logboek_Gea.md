# Logboek Casus A
### Logboek van Gea Bakker, behorende bij Casus A

##### Inleiding en taakverdeling
Voor de casus Dynamic Modelling (ODEs) hebben wij een python package ontwikkeld waarmee verschillende tumorgroeimodellen kunnen worden gesimuleerd, geoptimaliseerd en vergeleken met beschikbare tumorgroeidata.

Het project is uitgevoerd in samenwerking met Cheyenne Brouwer. We hebben de implementatie van de groeimodellen verdeeld. Ik was verantwoordelijk voor de Logistic- en Von Bertalanffy-modellen, terwijl Cheyenne de Exponential- en Gompertz-modellen heeft ontwikkeld. 

Daarnaast heb ik gewerkt aan de Euler-solver, de Hooke-Jeeves-optimalisatie, het vergelijken van de modellen en de README. Cheyenne heeft onder andere gewerkt aan de SciPy-solver, de Monte Carlo-optimalisatie en de Jupyter Notebook.

We hebben onze onderdelen samengevoegd tot één programma waarin de verschillende modellen, solvers en optimalisatiemethoden met elkaar kunnen worden vergeleken.

We hebben gebruikgemaakt van Github om onze code bij te houden, de code te delen en uiteindelijk om de code samen te voegen. Repository link: https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling.git

Gedurende de logboek wordt er verwezen naar specifieke commits die code bevatten voor het specifieke stuk.

##### Implementatie van de tumorgroeimodellen
Ik ben begonnen met het schrijven van de Logistic- en Von Bertalanffy-groeimodellen. Beide modellen beschrijven de verandering van het tumorvolume over de tijd, maar gebruiken hiervoor verschillende wiskundige vergelijkingen.

Het Logistic-model beschrijft tumorgroei waarbij de groeisnelheid afneemt naarmate het tumorvolume de draagcapaciteit nadert. Hiervoor worden de parameters r en K gebruikt, waarbij r de groeisnelheid bepaalt en K de draagcapaciteit.

Het Von Bertalanffy-model beschrijft de tumorgroei aan de hand van twee processen: groei en verlies. De parameter a bepaalt de bijdrage van de groei en de parameter b bepaalt de bijdrage van het verlies.

Ik heb beide modellen in eerste instantie bij elkaar gevoegd in een script. Later zijn deze uit elkaar gehaald in afzonderlijke scripts, zodat de code overzichtelijker en eenvoudiger aan te passen is. 

Daarnaast heb ik de algemene TumorGrowthModel-class ontwikkeld. Hierin worden onder andere de modelnaam, de groeifunctie en de bijbehorende parameters opgeslagen. Met de derivative()-methode kan de afgeleide van het tumorvolume bepaald worden. De derivative wordt later gebruikt door de numerieke solvers om de groeisnelheid op te vragen. Hierdoor kunnen de solvers voor alle groeimodellen op dezelfde manier worden gebruikt en hoef je bijvoorbeeld niet de solver aan te passen wanneer je een nieuwe tumorgroeimodel toevoegt.

Bijbehorende commits:
- Logistic and Von Bertalanffy model https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/1/changes/9ae4a8c0a254bb0b6be7096f4c7f5a9088c23431
- models/base_model.py https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/6/changes/ee454e7d409c4108a159121a657dda11816997d8

##### Implementatie van de Euler-solver
Na het implementeren van de groeimodellen ben ik verder gegaan met de Euler-solver. Deze solver geruikt de Euler-methode om een differentiaalvergelijking numeriek op te lossen.

De solver begint met een beginvolume en berekent vervolgens voor iedere tijdsstap het volgende tumorvolume. Hiervoor wordt de afgeleide van het groeimodel gebruikt. De afgeleide geeft aan hoe snel het tumorvolume op dat moment verandert. Door deze te vermenigvuldigen met de tijdsstap kan worden berekend hoeveel het volume verandert.

Ik heb de solver zo geschreven dat hij gebruik maakt van de derivative()-methode uit de TumorGrowthModel-class. Hierdoor kan dezelfde solver gebruikt worden voor alle vier de groeimodellen, zonder dat de code van de solver aangepast hoeft te worden.

De functie ontvangt het groeimodel, een tijdsinterval, het beginvolume en de tijdsstap. Vervolgens worden de berkende tijdstippen en tumorvolumes opgeslagen en teruggegeven.

Tijdens het ontwikkelen heb ik de Euler-solver getest om te controleren of de berekeningen goed verliepen en of de juiste waarden terug werden gegeven. Deze tests zijn geslaagd.

Bijbehorende commit:  De Euler-solver https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/9/changes/7b02ef4e38b82d6248155b9a8bbd8ea75c6e0e2f

##### Implementatie van Hooke-Jeeves
Voor het optimaliseren van de modelparameters heb ik de Hooke-Jeeves-methode geïmplementeerd. Het doel van deze methode is om de parameterwaarden te vinden waarmee het groeimodel zo goed mogelijk aansluit op de gemeten tumorvolume.

De optimizer begint met de oorspronkelijke parameterwaarden van het model. Vervolgens wordt per parameter geprobeerd om de waarde te verhogen of te verlagen met een bepaalde stapgrootte. Na iedere aanpassing wordt de Mean Squared Error (MSE) berekend om te controleren of de nieuwe parameters een betere voorspelling opleveren. 

Wanneer de MSE lager wordt, worden de nieuwe parameters opgeslagen. Als het verhogen en verlagen van een parameter geen verbetering oplevert, wordt de stapgrootte verkleind. Dit proces wordt herhaald totdat de stapgroottes onder de ingestelde tolerantie liggen.

Ik heb de optimizer zo gebouwd dat deze met verschillende groeimodellen en solvers kan werken. Hiervoor wordt gebruik gemaakt van de functie calculate_error(), die de voorspelde tumorvolumes vergelijkt met de gemeten waarden.

Tijdens het testen van de Hooke-Jeeves optimalizatie methode bleek dat het behoorlijk lang kon duren. Dit kwam doordat er nog steeds berekeningen werden uitgevoerd voor parameters waarvan de stapgrootte al kleiner was dan de tolerantie. 

Ik heb hiervoor een controle toegevoegd met continue, waardoor deze parameters worden overgeslagen. Bij een test met vier modellen en de Euler-solver werd de uitvoeringstijd hierdoor terugggebracht van 4413 seconden naar 3.39 seconden. 

De betreffende code:
            # Skip parameters when their step is below the tolerance, to cut down on processing time
            if abs(steps[key]) <= tolerance:
                continue

De gevonden parameters waren niet volledig gelijk aan die van de oorspronkelijke uitvoering. Dit laat zien dat de gekozen stopvoorwaarden invloed kunnen hebben op het uiteindelijke resultaat. De aanpassing zorgde er wel voor dat de optimalisatie veel sneller uitgevoerd kon worden. 

Bijbehorende commit: Implementatie Hooke-Jeeves: https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/10/changes/cca6e21f67d9fc178a2580adac066e5a00b8e805

##### Berekenen van de MSE en modelvergelijkingscriteria
Bij de implementatie van Hooke-Jeeves heb ik al beschreven dat de Mean Squared Error (MSE) wordt gebruikt om te bepalen of nieuwe parameterwaarden een betere voorspelling opleveren.

Voor het berekenen van de MSE wordt gebruikgemaakt van twee aparte functies: mse() en calculate_error(). De functie calculate_error() voert een simulatie uit met het opgegeven groeimodel, de solver en de parameterwaarden. Vervolgens vergelijkt mse() de voorspelde tumorvolumes met de gemeten waarden en berekent het gemiddelde van de gekwadrateerde verschillen.

Bij de Euler-solver worden de tumorvolumes berekend met een vaste tijdstap. Omdat de berekende tijdstippen niet altijd precies overeenkomen met de meettijdstippen, wordt np.interp() gebruikt om de voorspelde volumes op de juiste tijdstippen te bepalen. Bij de SciPy-solver kunnen de opgegeven meettijdstippen rechtstreeks worden gebruikt.

Naast de MSE heb ik ook de modelvergelijkingscriteria AICc en BIC geïmplementeerd. Deze criteria houden naast de fout van het model ook rekening met het aantal parameters. Hierdoor kunnen modellen met verschillende aantallen parameters met elkaar worden vergeleken.

Voor AICc en BIC heb ik afzonderlijke functies gemaakt, zodat deze vanuit het vergelijkingsscript kunnen worden aangeroepen.

De mse() en calculate_error() stonden in eerste instantie bij hooke_jeeves.py in het script, deze heb ik later in aparte scripts gezet.

Bijbehorende commits:
- MSE en calculate_error(): https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/13/changes/3084c7f495f740eefc9509c2bddfb4ff964d9a0b
- AICc en BIC: https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/11/changes/f9421e690b585f6897aa3ac4aaf74c160f1c4a24

##### Ontwikkeling van het vergelijkingsscript
Nadat de afzonderlijke onderdelen werkten, ben ik begonnen met het samenvoegen van de verschillende functies in model_comparison.py. Het doel van dit script is om de verschillende groeimodellen, numerieke solvers en optimalisatiemethoden automatisch met elkaar te vergelijken.

Ik heb hiervoor drie dictionaries aangemaakt waarin de vier groeimodellen, twee solvers en twee optimalisatiemethoden zijn opgenomen. Met behulp van geneste for-loops worden alle mogelijke combinaties doorlopen. Voor iedere combinatie worden de parameters geoptimaliseerd en vervolgens de MSE, AICc en BIC berekend.

De resultaten worden opgeslagen in een lijst van dictionaries. Vervolgens wordt deze lijst met Pandas omgezet naar een tabel, zodat de gebruiker de resultaten overzichtelijk in de terminal kan bekijken. Voor iedere tumor worden zestien combinaties doorgerekend.

Een belangrijk onderdeel van de opdracht was dat gebruikers hun eigen tumorgroeidata moeten kunnen gebruiken. Daarom heb ik het script aangepast, zodat de invoergegevens niet meer hardcoded zijn, maar via de commandline kunnen worden opgegeven. Met behulp van argparse kan de gebruiker via de terminal aangeven welk CSV-bestand gebruikt moet worden en welke kolommen de tumor-ID's, meettijdstippen en tumorvolumes bevatten.

Daarnaast heb ik een optioneel --tumor-id-argument toegevoegd. Hiermee kan de gebruiker één specifieke tumor analyseren. Wanneer dit argument niet wordt opgegeven, worden alle tumoren uit de dataset geanalyseerd. Ik heb ook een controle toegevoegd waardoor een duidelijke foutmelding wordt gegeven als de opgegeven tumor-ID niet bestaat.

Tijdens de ontwikkeling kreeg ik een foutmelding doordat de variabelen times en volumes nog niet waren gedefinieerd. Dit heb ik opgelost door de modelvergelijking onder te brengen in de aparte functie run_comparison() en de uitvoering te regelen vanuit main(). Hierdoor worden eerst de argumenten verwerkt en de dataset ingelezen voordat de modelvergelijking wordt gestart.

Bijbehorende commits:
- Ontwikkeling model_comparison.py: https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/16/changes/d1a0a28b4fa986549f3ca223d940b736394d5038
- Toevoegen terminalargumenten: https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/17/changes/fa590398ca0e6ca4f046d442c72524089bd24f23

##### Integratie van Monte Carlo en foutafhandeling
Toen de Monte Carlo-optimizer van Cheyenne aan het vergelijkingsscript werd toegevoegd, bleek dat Monte Carlo en Hooke-Jeeves precies dezelfde resultaten opleverden. Na het controleren van de code ontdekte ik dat binnen de loop nog rechtstreeks hooke_jeeves() werd aangeroepen. Hierdoor werd Hooke-Jeeves twee keer uitgevoerd.

Ik heb dit aangepast naar optimizer(), zodat de optimizer wordt uitgevoerd die op dat moment uit de dictionary wordt gehaald. Daarna leverden beide optimalisatiemethoden verschillende resultaten op.

Vervolgens ontstonden tijdens het uitvoeren van Monte Carlo numerieke fouten. Sommige willekeurige parametercombinaties veroorzaakten ongeldige berekeningen in de groeimodellen.

Bij Von Bertalanffy ontstond een waarschuwing doordat een negatief tumorvolume werd gebruikt in een machtsberekening. Bij Gompertz ontstond een math domain error, doordat een ongeldige waarde in de logaritme terechtkwam.

Om deze problemen op te lossen heb ik calculate_error() uitgebreid met foutafhandeling. Met een try-except worden bepaalde numerieke fouten opgevangen. Daarnaast wordt gecontroleerd of de voorspelde tumorvolumes eindige waarden bevatten en of er negatieve volumes voorkomen.

Ook wordt gecontroleerd of de berekende MSE een geldige waarde is. Wanneer een parametercombinatie een ongeldige berekening veroorzaakt, wordt een oneindige MSE teruggegeven. Hierdoor kunnen de optimizers deze combinatie afwijzen en verder zoeken naar betere parameters.

Na deze aanpassingen kon de vergelijking voor de geteste tumor met beide optimalisatiemethoden worden uitgevoerd.

Bijbehorende commits:
- Integratie Monte Carlo en foutafhandeling: https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/18/changes/9195dad1f0af147633360f8b9faf553e0a1e4ce1

##### Testen van het volledige programma en documentatie
Om het volledige programma te controleren heb ik verschillende tests uitgevoerd met de synthetische tumordataset. Voor de uiteindelijke controle heb ik tumor Model1_101 geselecteerd.

Het programma doorliep alle vier de groeimodellen met beide numerieke solvers en optimalisatiemethoden. Dit leverde zestien resultaten op, waarbij voor iedere combinatie de gevonden parameters, MSE, AICc en BIC werden weergegeven.

Tijdens deze test viel op dat Monte Carlo bij verschillende modellen een lagere MSE vond dan Hooke-Jeeves. Vooral bij Logistic en Gompertz waren duidelijke verschillen zichtbaar. Het Exponential-model met de SciPy-solver en Hooke-Jeeves behaalde bij deze uitvoering de laagste MSE, AICc en BIC.

De resultaten laten zien dat de keuze van de optimalisatiemethode invloed kan hebben op de gevonden parameters. Daarbij moet rekening worden gehouden met het feit dat Monte Carlo willekeurige parameterwaarden gebruikt en dus bij een volgende uitvoering andere resultaten kan opleveren.

Daarnaast heb ik gecontroleerd of het programma via de terminal kon worden uitgevoerd. Met --help werden de beschikbare argumenten weergegeven en ook de controle op een niet-bestaande tumor-ID werkte.

Ik heb de README geschreven met uitleg over de installatie, het gebruik en de structuur van het package. Daarnaast heb ik achtergrondinformatie toegevoegd over de gebruikte modellen en technieken, inclusief referenties.

Readme: https://github.com/cheyennebrouwer/Casus_Dynamic-Modelling/pull/21/changes/cd8b517b4974a4f3b90a1e6647621644a9ce7cc0
