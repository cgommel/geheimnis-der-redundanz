# Schreibstil-Leitfaden

> Die Tonalität des Tutorials ist genauso wichtig wie der Inhalt. Das Heft soll sich anfühlen wie eine kompetente, etwas augenzwinkernde Begleitung, nicht wie ein Schulbuch.

## Grundton

- **Direkte Ansprache an Greta** in der zweiten Person Singular („du", nicht „man" oder „wir lösen jetzt …"). Wir-Form ist nur dort okay, wo sie Gemeinschaftlichkeit vermittelt („Heute schauen wir uns an …").
- **Warm, ermutigend, ohne herablassend zu sein.** Greta ist klug und neugierig; das Heft soll sie ernst nehmen.
- **Augenzwinkern erlaubt**, aber sparsam. Trockene Bemerkungen sind besser als Slapstick. Beispiele aus den bestehenden Heften:
  - „Das `61` im siebten Kapitel ist Pflichtlektüre für jede Informatikerin." (Anspielung auf Hofstadter)
  - „Probiere mehrere. Findest du einen, den EAN-13 *nicht* erkennt?"
  - „Hat Greta das gemerkt?" (in einer Lösung, wo *kein* Fehler vorlag)
- **Keine Plattitüden** wie „Wie wir alle wissen" oder „Klarerweise". Wenn etwas schwer ist, sagen wir es: „Das ist der Knaller …" oder „Das ist der schwierigste Schritt heute, lass dir Zeit."

## Didaktische Prinzipien

### Selbstentdecken statt Frontalbelehrung

Der Lerner soll möglichst viele Aha-Momente *selbst* haben. Beispiele aus den bestehenden Heften:

- Tag 1: Greta entdeckt durch Brute-Force-Test selber, dass EAN-13 Zifferndreher mit Differenz 5 nicht erkennt.
- Tag 2: Greta beweist (mit Tipps an der Hand) selber, warum ISBN-10 *alle* Zifferndreher erkennt.
- Tag 3: Der Aha-Moment ist, wenn die drei Prüfsummen binär gelesen genau die Position des Fehlers ergeben — das wird *nach* dem ersten Selber-Bauen erklärt, nicht davor.

### Bleistift vor Python

Jedes Konzept wird zuerst von Hand auf Karopapier durchgegangen, dann in Python geübt. Das stellt sicher, dass Greta versteht, was passiert, und nicht nur Code abtippt.

### Cliffhanger zwischen den Tagen

Jeder Tag endet mit einer Vorausschau und idealerweise einer **Knobelaufgabe**, die zum nächsten Tag überleitet. Beispiele:

- Tag 2 → Tag 3: „Wie viele Prüfbits brauchst du mindestens für 1-Bit-Korrektur bei 4 Datenbits?"
- Tag 3 → Tag 4: „Was passiert, wenn 2 oder mehr benachbarte Bits gekippt sind?"
- Tag 4 → Tag 5: „Wie könnte man Modulo auf Bytes (statt Bits oder Ziffern) übertragen?"

## Konkrete Sprach-Konventionen

### Sprache

- Deutsch, Sie-Form für niemanden, Du-Form für Greta.
- Anglizismen sparsam und nur, wenn sie Standard sind: „Bitfehler" (nicht „bit error"), aber „Burst Error" als Klammerzusatz wenn Fachbegriff: *Bündelfehler (engl. burst errors)*.
- Mathematische Begriffe deutsch, mit englischer Klammer beim Erstauftauchen, falls relevant: *Mindestdistanz (engl. minimum distance)*.

### Hervorhebungen

- **Fett** für zentrale Begriffe beim Erstauftauchen oder zur betonten Wiederaufnahme.
- *Kursiv* für sanfte Betonung („das ist *nicht* die Lösung") oder Fremdwörter.
- `Monospace` für Python-Code, Bitfolgen, Codewörter, Zahlen mit Sonderbedeutung im Kontext.
- Quote-Blöcke (`>`) für Tipps, Hinweise, kurze Warnungen.

### Aufgaben-Konventionen

Im Markdown gibt es drei Aufgabentypen, die durch Emoji-Marker am Anfang einer `###`-Überschrift erkannt werden:

- `### ✏️ Bleistiftübung N – Titel` für Übungen mit Stift und Papier
- `### 💻 Python-Einheit N – Titel` für Code-Übungen in Thonny
- `### 🛠️ Werkzeug-Check: Titel` für Werkzeug-Einrichtung (z. B. Thonny installieren)

Diese Marker werden im Build-Schritt vom Postprozessor in **Marginalien** (Randnotizen) verwandelt.

Innerhalb einer Aufgabe können Unteraufgaben nummeriert werden mit `(a)`, `(b)`, `(c)`. Tiefere Unter­aufgaben mit `Aufgabe N.M – Untertitel`.

### Nummerierung der Aufgaben

Bleistiftübungen und Python-Einheiten werden **innerhalb eines Tages** durchnummeriert (Bleistiftübung 1, 2, 3 …; Python-Einheit 1, 2, 3 …). Die Nummerierung beginnt bei jedem neuen Tag wieder bei 1.

Im Lösungsteil (am Ende jedes Tages) werden die Lösungen in derselben Reihenfolge präsentiert, mit derselben Nummerierung, aber ohne den Emoji-Marker (das verhindert, dass im Lösungsteil ebenfalls Marginalien generiert werden).

## Praxisbezüge

Konkrete Praxisbezüge sind das Herzstück. Sie erden die Mathematik. Beispiele aus den bestehenden Heften:

- Tag 1: EAN-13 auf einer Schokoladenpackung, die Greta selbst von der Küche holt.
- Tag 2: ISBN-10 auf einem alten Buch aus dem Regal („Gödel, Escher, Bach" als kleine Anekdote).
- Tag 2: Luhn-Algorithmus auf Kreditkarten — und der wichtige Disclaimer „Prüfziffer ≠ Sicherheit".
- Tag 3: Hammings persönliche Frustration mit Lochkarten am Wochenende.
- Tag 3: ECC-RAM, Voyager, WLAN, SSDs als reale Anwendungen.
- Tag 4: Zerkratzte CDs und Funkfading als Bündelfehler-Beispiele; CIRC auf Audio-CDs als Vorgriff auf Reed-Solomon.

**Ziel:** Greta soll am Ende von Tag 1 wissen, dass auf jeder Schokoladenpackung Mathematik steckt; am Ende von Tag 10, dass jedes Smartphone ihre Lieblingsmusik nur deshalb verzerrungsfrei abspielen kann, weil im Hintergrund Reed-Solomon läuft.

## Was der Stil *nicht* sein soll

- Keine pseudo-amerikanische „You can do it!"-Energie.
- Kein Schulbuch-Förmlichkeit („Wir betrachten nun den Fall, dass …").
- Keine reine Faktenliste. Wenn ein Konzept eingeführt wird, gibt es immer eine kleine Geschichte oder einen konkreten Anlass.
- Keine ironische Distanzierung von der Mathematik („Klingt kompliziert, ist aber egal"). Die Mathematik ist das Hauptthema, nicht eine notwendige Übel.

## Lösungsteil

- Beginnt immer auf einer **frischen Seite** (`\newpage` direkt vor `# 📘 Lösungen …`).
- Reihenfolge wie im Aufgabenteil.
- Lösungen sollen **nicht zu knapp** sein – auch der Rechenweg kann interessant sein.
- Wo sinnvoll: zusätzliche Erklärung *warum* die Lösung funktioniert, nicht nur *was* die Lösung ist.

## Längen-Faustregeln

- Ein Tag → ungefähr **2 bis 3 Stunden** Bearbeitungszeit für Greta.
- Ein Tag → ungefähr **10 bis 16 Seiten** im PDF inklusive Lösungen.
- Pro Tag etwa **4 bis 8 Aufgaben** (Bleistift + Python kombiniert).
- Lernziele am Anfang: **5 bis 7 Bullet-Points**, jeder konkret testbar.
- Reflexion am Ende: **3 Fragen zum Mitnehmen**, die zum Weiterdenken anregen.
