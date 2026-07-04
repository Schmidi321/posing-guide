// Posen-Datenbank für den Posing-Guide
// shootType: 'couple' | 'family' | 'single'

const SHOOT_TYPES = [
  { key: 'couple', label: 'Brautpaar' },
  { key: 'family', label: 'Familie & Gruppen' },
  { key: 'single', label: 'Einzelperson' },
];

const CATEGORY_LABELS = {
  stehend: 'Stehend',
  gehen: 'Gehen & Bewegung',
  naehe: 'Nähe & Emotion',
  candid: 'Lachen & Candid',
  kreativ: 'Kreativ',
  aufstellung: 'Aufstellung',
  grossgruppe: 'Großgruppe',
  kinder: 'Kinder',
  sitzend: 'Sitzend',
  detail: 'Details',
  bewegung: 'Bewegung',
};

const POSES = [
  // ---------------- BRAUTPAAR ----------------
  { id: 'c01', shootType: 'couple', category: 'stehend', title: 'Klassisch frontal', instruction: 'Beide stehen sich zugewandt, Hände auf Hüfte oder Brust des Partners. Sag: "Schaut euch tief in die Augen."', tip: 'Gewicht auf hinteres Bein verlagern lassen, wirkt schlanker.' },
  { id: 'c02', shootType: 'couple', category: 'stehend', title: 'Drei-Viertel-Ansicht', instruction: 'Paar leicht seitlich zueinander, vorderer Fuß zeigt zur Kamera. Blick zueinander oder in die Kamera.', tip: 'Nie beide Schultern parallel zur Kamera – wirkt breiter.' },
  { id: 'c03', shootType: 'couple', category: 'stehend', title: 'Stirn an Stirn', instruction: 'Beide zugewandt, Stirnen berühren sich, Augen geschlossen. Sag: "Atmet tief durch und lächelt leise."', tip: 'Von schräg unten wirkt es romantischer.' },
  { id: 'c04', shootType: 'couple', category: 'stehend', title: 'Rückenlehnen', instruction: 'Eine Person lehnt sich mit dem Rücken an die andere, beide schauen in die Kamera oder aneinander vorbei.', tip: 'Gut für Silhouetten vor Fenstern oder Sonnenuntergang.' },
  { id: 'c05', shootType: 'couple', category: 'stehend', title: 'Dip / Tanzhaltung', instruction: 'Eine Person lässt die andere leicht nach hinten sinken, wie beim Tanzabschluss.', tip: 'Kurz vorher üben lassen wegen Balance – Sicherheit geht vor.' },
  { id: 'c06', shootType: 'couple', category: 'gehen', title: 'Hand in Hand gehen', instruction: 'Paar geht einen Weg entlang, Hände verschränkt, Blick nach vorne oder zueinander. Mehrfach wiederholen lassen.', tip: 'Von vorne rückwärts gehend fotografieren für natürliche Bewegung.' },
  { id: 'c07', shootType: 'couple', category: 'gehen', title: 'Auf die Kamera zu', instruction: 'Beide laufen Hand in Hand direkt auf dich zu, im letzten Moment lachen oder anhalten lassen.', tip: 'Serienbildmodus nutzen, bester Moment ist meist die Bewegung.' },
  { id: 'c08', shootType: 'couple', category: 'gehen', title: 'Wegdrehen und zurückschauen', instruction: 'Beide gehen ein paar Schritte weg von der Kamera, drehen sich dann gemeinsam um und schauen zurück.', tip: 'Funktioniert super mit langer Schleppe oder Anzugjacke im Wind.' },
  { id: 'c09', shootType: 'couple', category: 'gehen', title: 'Drehung / Twirl', instruction: 'Eine Person dreht die andere einmal um die eigene Achse, Kleid schwingt mit.', tip: 'Am besten mit etwas Abstand fotografieren, damit die Bewegung reinpasst.' },
  { id: 'c10', shootType: 'couple', category: 'gehen', title: 'Verfolgungsspiel', instruction: 'Eine Person läuft leicht lachend voraus, die andere folgt mit ausgestreckter Hand.', tip: 'Gibt lockere, candid wirkende Bilder – gut nach steifen Posen.' },
  { id: 'c11', shootType: 'couple', category: 'naehe', title: 'Umarmung von hinten', instruction: 'Eine Person umarmt die andere von hinten, Kinn auf der Schulter, beide schauen in dieselbe Richtung.', tip: 'Gut für Landschaft im Hintergrund.' },
  { id: 'c12', shootType: 'couple', category: 'naehe', title: 'Flüstern ins Ohr', instruction: 'Eine Person flüstert der anderen etwas ins Ohr, echtes Lachen provozieren mit einer lustigen Ansage.', tip: 'Sag ihnen einen Insider-Satz zum Nachsprechen, wirkt authentischer.' },
  { id: 'c13', shootType: 'couple', category: 'naehe', title: 'Kuss auf die Stirn', instruction: 'Eine Person küsst die andere auf die Stirn, die geküsste Person schließt die Augen und lächelt.', tip: 'Leicht von unten fotografieren, betont die Geste.' },
  { id: 'c14', shootType: 'couple', category: 'naehe', title: 'Hand am Gesicht', instruction: 'Eine Person legt die Hand sanft an die Wange der anderen, Blickkontakt.', tip: 'Auf saubere Fingerhaltung achten, keine verkrampfte Hand.' },
  { id: 'c15', shootType: 'couple', category: 'naehe', title: 'Der Kuss', instruction: 'Klassischer Kuss, Kopf der einen Person leicht geneigt, freie Hand am Gesicht oder Nacken.', tip: 'Mehrere Varianten schießen: Profil, von der Seite, von oben.' },
  { id: 'c16', shootType: 'couple', category: 'candid', title: 'Privater Witz', instruction: 'Frag nach einer lustigen gemeinsamen Erinnerung, während du fotografierst – echtes Lachen einfangen.', tip: 'Kamera schon hochhalten bevor die Frage kommt.' },
  { id: 'c17', shootType: 'couple', category: 'candid', title: 'Kitzeln / Necken', instruction: 'Eine Person neckt die andere spielerisch (kitzeln, ins Ohr pusten), Reaktion einfangen.', tip: 'Serienbild, der beste Moment kommt meist nach dem ersten Lachen.' },
  { id: 'c18', shootType: 'couple', category: 'candid', title: 'Gemeinsam auf etwas schauen', instruction: 'Beide schauen gemeinsam auf etwas außerhalb des Bildes (Ring, Handy, Landschaft) und reagieren natürlich.', tip: 'Erzeugt Tiefe, weil niemand direkt in die Kamera schaut.' },
  { id: 'c19', shootType: 'couple', category: 'kreativ', title: 'Silhouette', instruction: 'Paar vor helle Lichtquelle (Sonnenuntergang, Fenster) stellen, Umriss/Kuss als Silhouette.', tip: 'Gegen das Licht belichten, Motiv unterbelichtet lassen.' },
  { id: 'c20', shootType: 'couple', category: 'kreativ', title: 'Spiegelung / Reflexion', instruction: 'Pfütze, Fenster oder Spiegel nutzen, Paar und Spiegelbild im Bild.', tip: 'Kamera tief halten für symmetrische Spiegelungen.' },
  { id: 'c21', shootType: 'couple', category: 'kreativ', title: 'Weitwinkel mit Umgebung', instruction: 'Paar klein im Bild, Location/Architektur/Natur dominiert das Bild.', tip: 'Gute Führungslinien in der Location suchen (Wege, Mauern, Alleen).' },
  { id: 'c22', shootType: 'couple', category: 'kreativ', title: 'Regenschirm / Requisite', instruction: 'Vorhandene Requisite einbauen (Schirm, Fahrrad, Auto, Blumen) für ein Bild mit Geschichte.', tip: 'Nur nutzen wenn es zur Location/zum Paar passt, nicht erzwingen.' },

  // ---------------- FAMILIE & GRUPPEN ----------------
  { id: 'f01', shootType: 'family', category: 'aufstellung', title: 'Klassische Reihen', instruction: 'Große Gruppe in 2-3 Reihen, große Personen hinten/außen, kleine vorne/mittig. Alle leicht zur Kamera gedreht.', tip: 'Immer 2-3 Aufnahmen machen – irgendwer blinzelt garantiert.' },
  { id: 'f02', shootType: 'family', category: 'aufstellung', title: 'Halbkreis um Brautpaar', instruction: 'Brautpaar in der Mitte, Familie im Halbkreis darum, leicht nach innen gedreht.', tip: 'Brautpaar leicht erhöht platzieren (Stufe), damit es nicht untergeht.' },
  { id: 'f03', shootType: 'family', category: 'aufstellung', title: 'Kernfamilie', instruction: 'Nur Eltern + Brautpaar (bzw. Geschwister), enger zusammenstehen, Arme umeinander.', tip: 'Diese Aufnahme zuerst machen, danach lösen sich oft welche ab.' },
  { id: 'f04', shootType: 'family', category: 'aufstellung', title: 'Brautpaar mit je einer Seite', instruction: 'Erst nur Familie der Braut mit dem Paar, dann nur Familie des Bräutigams – getrennt fotografieren.', tip: 'Spart Zeit: während eine Seite postiert wird, die andere schon vorbereiten lassen.' },
  { id: 'f05', shootType: 'family', category: 'grossgruppe', title: 'Alle Gäste', instruction: 'Ganze Hochzeitsgesellschaft auf Stufen, Hügel oder mit Leiter von erhöhter Position fotografieren.', tip: 'Laut und klar ansagen, wann geschaut werden soll – Timing zählt hier am meisten.' },
  { id: 'f06', shootType: 'family', category: 'grossgruppe', title: 'Von oben fotografiert', instruction: 'Gruppe liegt oder sitzt im Kreis/auf dem Boden, du fotografierst von einer Leiter oder erhöhten Stelle senkrecht von oben.', tip: 'Braucht Erlaubnis für erhöhten Standpunkt – vorher klären.' },
  { id: 'f07', shootType: 'family', category: 'grossgruppe', title: 'Wurf-Moment', instruction: 'Konfetti, Hüte oder Reis gemeinsam in die Luft werfen lassen, im Sprung/Fallen fotografieren.', tip: 'Countdown "3-2-1-Wurf!" laut ansagen, Serienbild nutzen.' },
  { id: 'f08', shootType: 'family', category: 'candid', title: 'Lachen provozieren', instruction: 'Der Gruppe sagen: "Winkt eurem schlimmsten Feind zu" oder ähnlichen Unsinn – echtes Lachen entsteht.', tip: 'Funktioniert fast immer besser als "alle bitte lächeln".' },
  { id: 'f09', shootType: 'family', category: 'candid', title: 'Gespräch im Kreis', instruction: 'Gruppe natürlich im Kreis stehen und reden lassen, unauffällig von der Seite fotografieren.', tip: 'Nicht ankündigen, dass fotografiert wird – wirkt am echtesten.' },
  { id: 'f10', shootType: 'family', category: 'candid', title: 'Umarmung spontan', instruction: 'Zwei Personen bitten sich kurz und herzlich zu umarmen, mittendrin auslösen statt danach.', tip: 'Auf den Moment kurz vor dem Loslassen warten, meist der schönste.' },
  { id: 'f11', shootType: 'family', category: 'kinder', title: 'Kinder auf Schultern', instruction: 'Ein Elternteil trägt das Kind huckepack oder auf den Schultern, beide lachen.', tip: 'Kinder kurz vorher albern machen lassen für echte Freude.' },
  { id: 'f12', shootType: 'family', category: 'kinder', title: 'Kinder rennen lassen', instruction: 'Kinder eine kurze Strecke auf die Kamera zu rennen lassen (z.B. zu den Eltern).', tip: 'Tiefe Kamera-Position (auf Augenhöhe der Kinder) wirkt am stärksten.' },
  { id: 'f13', shootType: 'family', category: 'kinder', title: 'Großeltern mit Enkeln', instruction: 'Großeltern sitzend, Enkelkinder auf dem Schoß oder daneben kuscheln lassen.', tip: 'Ruhige, langsame Anweisungen – wirkt entspannter auf ältere Gäste.' },

  // ---------------- EINZELPERSON ----------------
  { id: 's01', shootType: 'single', category: 'stehend', title: 'Klassisches Portrait', instruction: 'Drei-Viertel-Drehung zur Kamera, Gewicht auf hinteres Bein, Kinn leicht nach vorne/unten.', tip: 'Kinn leicht senken vermeidet Doppelkinn-Effekt.' },
  { id: 's02', shootType: 'single', category: 'stehend', title: 'Hand in der Tasche', instruction: 'Eine Hand locker in Hosen-/Jackentasche, andere Seite des Körpers offen zur Kamera.', tip: 'Wirkt entspannt und lässig, gut für Bräutigam-Solo.' },
  { id: 's03', shootType: 'single', category: 'stehend', title: 'Blick über die Schulter', instruction: 'Person steht mit Rücken zur Kamera, dreht Kopf und Oberkörper leicht zurück zur Kamera.', tip: 'Zeigt Kleid/Anzug von hinten und Gesicht gleichzeitig.' },
  { id: 's04', shootType: 'single', category: 'stehend', title: 'An Wand/Baum gelehnt', instruction: 'Locker mit Schulter an Wand oder Baum lehnen, ein Bein leicht angewinkelt.', tip: 'Achte auf saubere Linie der Wirbelsäule, nicht zu eingesackt.' },
  { id: 's05', shootType: 'single', category: 'sitzend', title: 'Auf Stufen sitzend', instruction: 'Person sitzt auf Treppenstufen, Ellenbogen auf Knien oder Hände locker gefaltet.', tip: 'Von leicht unten fotografieren wirkt eleganter.' },
  { id: 's06', shootType: 'single', category: 'sitzend', title: 'Auf Bank/Stuhl', instruction: 'Seitlich auf Sitzfläche, ein Arm über die Lehne, Blick entspannt zur Seite oder Kamera.', tip: 'Beine überkreuzen für schlankere Silhouette.' },
  { id: 's07', shootType: 'single', category: 'sitzend', title: 'Am Boden, Kleid drapiert', instruction: 'Braut setzt sich vorsichtig auf den Boden/Stufen, Kleid wird großzügig um sie herum drapiert.', tip: 'Kleid immer nach dem Hinsetzen noch einmal in Form ziehen.' },
  { id: 's08', shootType: 'single', category: 'bewegung', title: 'Gehen auf die Kamera zu', instruction: 'Person läuft locker auf dich zu, Arme natürlich mitschwingen lassen, nicht auf die Füße schauen.', tip: 'Mehrfach wiederholen, oft ist der 3. oder 4. Versuch am natürlichsten.' },
  { id: 's09', shootType: 'single', category: 'bewegung', title: 'Drehung im Kleid', instruction: 'Braut dreht sich einmal um die eigene Achse, Kleid/Schleier schwingt mit, im Schwung auslösen.', tip: 'Serienbildmodus, den Höhepunkt des Schwungs erwischen.' },
  { id: 's10', shootType: 'single', category: 'bewegung', title: 'Haar/Schleier im Wind', instruction: 'Bei Wind oder mit leichtem Werfen Haare/Schleier in Bewegung bringen, Moment einfangen.', tip: 'Gegen den Wind fotografieren, damit Haare zur Kamera wehen.' },
  { id: 's11', shootType: 'single', category: 'detail', title: 'Ringe', instruction: 'Nahaufnahme der Hände mit Ring, evtl. ineinander verschränkt oder auf einer Fläche drapiert.', tip: 'Makro-Objektiv oder naher Fokus, weiches Licht von der Seite.' },
  { id: 's12', shootType: 'single', category: 'detail', title: 'Schleier/Kleid-Detail', instruction: 'Nahaufnahme von Spitze, Knöpfen oder Stoffstruktur des Kleides.', tip: 'Auf saubere, faltenfreie Stelle achten.' },
  { id: 's13', shootType: 'single', category: 'detail', title: 'Schuhe', instruction: 'Schuhe einzeln oder am Fuß in Szene setzen, z.B. auf einer Treppe oder im Detail.', tip: 'Gutes Licht wichtiger als komplizierte Anordnung.' },
];

const PHASE_PLANS = {
  couple: [
    { name: 'Ankommen & Lockerung', fraction: 0.15, categories: ['candid'] },
    { name: 'Klassische Posen', fraction: 0.30, categories: ['stehend'] },
    { name: 'Bewegung', fraction: 0.20, categories: ['gehen'] },
    { name: 'Nähe & Emotion', fraction: 0.25, categories: ['naehe'] },
    { name: 'Kreativ / Abschluss', fraction: 0.10, categories: ['kreativ'] },
  ],
  family: [
    { name: 'Große Gruppe formal', fraction: 0.30, categories: ['grossgruppe', 'aufstellung'] },
    { name: 'Kernfamilie', fraction: 0.25, categories: ['aufstellung'] },
    { name: 'Candid & Lachen', fraction: 0.25, categories: ['candid'] },
    { name: 'Kinder einbeziehen', fraction: 0.20, categories: ['kinder'] },
  ],
  single: [
    { name: 'Stehend', fraction: 0.30, categories: ['stehend'] },
    { name: 'Sitzend / Ruhig', fraction: 0.25, categories: ['sitzend'] },
    { name: 'Bewegung', fraction: 0.25, categories: ['bewegung'] },
    { name: 'Details', fraction: 0.20, categories: ['detail'] },
  ],
};
