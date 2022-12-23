Title: Tèrnaru
Status: published
Menu: no

Consider this an attempt to remake my old Tèrnaru language from scratch.

## Overview

The language is primarily isolating, and has a SOV typology, though it
displays remnants of an ancestor language with VSO typology,
particularly in the initial complex, which is a fossilised auxiliary
verb. Its morphosyntactic alignment resembles that found in Austronesian
alignment, but also resembles that of fluid-S languages.

## Phonology

The transcription method used in this document is *not* the language’s
native orthography and is only a latinisation for convenience.

The phonology of the language is relatively simple.

### Vowel system

There are nine vowels. The schwa only occurs in unstressed syllables.

```text
i       u
 e  ə  o
  ɛ   ɔ
   a ɑ
```

Orthographically, these are realised as:

```text
i       u
 e  y  o
  è   ò
   a á
```

‘y’ might appear to be an odd choice to represent schwa, but I’m Irish
and I’m familiar with Welsh and Manx, so it’s not odd to me. The choice
of the grave accent for lowering and thus ‘è’ and ‘ò’ to represent /ɛ/
and /ɔ/ is based on Romance languages. My choice of ‘á’ to represent /ɑ/
is based loosely Irish and the fact that I needed some reasonable choice
to represent the sound and recycling the grave accent didn’t seem
appropriate. Other possibilities would’ve been to use the trema or the
circumflex, but both would’ve had their own issues.

### Consonants

The consonant system is similarly simple:

```text
           Bil    Alv  Ret  Vel
           U  V   U V    V  U V
Stop       p  b   t d       k g
Fricative  f  v   s z
Nasal         m          n
Flap                          r
Lat. App.                l
```

/f/ can be realised as either [f] or [ɸ] and /v/ as [v] or [β].
They’re generally realised bilabially. /s/ can be realised [ʃ] or
[s] and /z/ and be realised as [ʒ] or [z]. Both are generally
realised as alveolar consonants. [h] is occasionally used to prevent
hiatus, but is not written.

### Phonotatics

To do.

## Some sample sentences

```text
?       fè  ták
?       βe  tɑk
MID.PST 1sg hit
'I hit myself'
```

## Earlier version

### A Note Before You Continue

This is the language sketched circa January 2001. At the time of writing, that makes this three and a half years out of date. It’s not that stuff has changed, just that this leaves a lot of the language’s details out.

It’s about time I put this thing up here though: I should have done this a long time ago.

### Basic Syntax

The various phrases of the sentence can roam freely and have no set position asides from the trend of the subject/topic being the first item in the sentence and the verb complex being last, making it an SOV language.

There is a growing tendancy towards making sentences VSO. If so, the Verbal Particle sits _after_ the verb, otherwise it tends to come _before_ the verb. Relative clauses are always SOV.

### Verbs

The verb in Térnaru is generally the last item in the sentence. It is accompanied by a particle called the _Verbal Particle_ (VP). The verb itself takes very few inflections, except for clause nominalisation in the creation of relative clauses, deriving the gerund and verbal adjective, and in deriving the imperative forms of the verb.

Where the sentence is topicalised, the VP or any other element may come between the verb and the case particles of the topicalised NP, e.g.

"As for me, I was happy":

     (1) Vé íl a-gílt
         1SG PST EXP-be.happy
    *(2) Vé  al-íl   gílt
         1SG EXP-PST be.happy

(1) is a well-formed sentence; (2) is not. This is because the particle _a_, which marks the Absolutive case is seperated from the verb _gílt_ (_be happy_) by the VP—_íl_—marking the sentence as being in the past tense.

Inflections upon verbs are usually for the purpose of derivation—creating a wholly new verb, noun, or adjectiv—except in the case of the nominalising suffix _-un_, used in forming relative clauses, and the suffix _-ya_ to make verb imperative (th only mood not indicated on the VP).

The singular imperative is indicated with the suffix _-iés_. The plural imperative is indicated with the suffix _-nu_ which causes a complex degree of mutation on the preceeding consonants. I’ll outline this when I have time.

The gerund is formed with the suffix _-dwé_; the verbal adjective from the gerund + _-in_, e.g.

    dyoren  >  dyorendé  >  dyorendwin
    fall       falling      fallen

The agent noun is formed with the prefix _il-_ and affects the voicing of the following consonant by making it unvoiced, e.g.

    tak  >  iltak
    hit     hitter (one who hits)

The patient noun is similarly formed to the agent noun with the prefix _in-_ and affects the voicing of the following consonant by making it voiced, e.g.

    tak   >  indak
    hit      hitee (one who is hit)

The VP may be placed virtually anywhere in the sentence, so long as it doesn’t split any NPs or seperate a topic’s case particles from the verb.

The form of the VP is:

    P-Ø-A-B

where _Ø_ indicates the null morpheme acting as the root to which all other affixes are attached.

The only currently known type-P prefix is _s-_. This indicates the sentence is interrogative.

Type-1 suffixes indicate tense and are _-íl_ (Past), _-(e)_ (Present, the _e_ is epethentic), _-en_ (Future), and _-at_ (Abstract).

Type-2 suffixes indicate mood and are _-né_ (Ability), _-wa_ (Need), _-ié_ (Intent), _-an_ (Appropriateness/Trueness), _-té_ (Subjunctive: doubt/assumption) and, _-ur_ (Optative: wish). Note though that _-en + -né = -enté_ and _-at + -té = -asé_.

### Noun Phrases (NPs)

Each NP except the topic has a Case Particle (CP), or preposition if you prefer, to denote their purpose in relation to the rest of the sentence. This particle comes before its NP. An NP may have more than one particle in front of it if it serves more than one purpose in the sentence, e.g. if the sentence is reflexive, a sentence such as

    (3) an-a-Lídu    íl  ták
        ACT-PAT-Lídu PST hit
        "Lídu hit himself" (assuming Lídu is male)

is perfectly valid.

Other than that, adjectives follow the nouns they govern; direct and indirect relative clauses follow the NPs the govern too; numbers preceed the noun, between the CP and the noun.

Pluralisation is indicated with the suffix _-í_. Between the noun and the pluralisation suffix come the determiners.

Nouns are by default indefinite. When affixing a determiner, in some cases the epethentic vowel _e_ is introduced. In other cases it’s not, with the determiner causing some sort of mutation in the preceeding letters.

The determiners are _-d-_ (Definite/Demonstrative: this/these), _-r-_ (Definite/Demonstrative: that/those), and _-w-_ (Partitive).

Where _-d-_ occurs after a liquid, rhotic, glide or vowel, no change occurs. When it occurs after a nasal consonant, that nasa consonant becomes _n_. If it occurs after _t_ or _d_, it becomes _s_, e.g. _érakwant_ \> _érakwans, érakwansí_. Otherwise the epethentic vowel _e_ is inserted.

Where _-w-_ follows a _w_, it becomes _l_, e.g. _éw_ \> _élwí_. In the singular, if _-w-_ is not preceeded by a vowel, _a_ is added at the end, e.g. _éw_ \> _élwí_.

Following an _r_, _-r-_ becomes _-l-_, e.g. _alvír_ \> _alvírla, alvírí_.

The posessives are affixed after the plural affix, if any. They are:

| Affix | Role |
| -- | -- |
| -éva | My |
| -avu | Our (incl.) |
| -ava | Our (excl.) |
| -ésu | Your (sg.) |
| -asu | Your (pl.) |
| -ant | Their (sg.) |
| -ans | Their (pl.) |
| -amé | Ones |

The pronouns are:

| Pronoun | Role |
| -- | -- |
| vé | Me |
| vésí | We (incl.) |
| vésa | We (excl.) |
| su | You (sg.) |
| ssí | You (pl.) |
| lís | Them (sg.) |
| yéq | Them (pl.) |
| kesé | One |

### Case Markers

Here’s an incomplete list of the case markers. The letter given in brackets is now epethentic, but was once part of particle and only now appears to prevent hiatus.

| Particle | Role |
| -- | -- |
| Experiencer/Patient | a(l) |
| Actor | an(i) |
| Oblique | wa(s) |
| Genitive | u(l) |
| Relational | kké(s) |
| Vocative | es |

The relational marker means from, of, related to, associated with, etc...

In intransitive sentences, the Actor marker is used to mark an active subject, i.e. one who willingly/voluntarily takes part (‘I slid across the ice’—I made myself slide on it), whereas the Experiencer marker is used to mark an passive subject, i.e. one who does not take part of their own will (‘I was slid across the ice’—Someone else made me slide on it).

### Relative Clauses

Relative Clauses are essentially nominalised sentences. They are always topicalised, with the topic at the beginning—being the NP governed by the clause—and ending with a nominalised verb. This is similar to the way Japanese relative clauses work.

Example:

    (4) Tagas       a-Lídu   íl  al-abrírun
        information ACT-Lídu PST PAT-desire-NMLS
        "The information that Lidu wanted"

### Numbers

I have this described, but I don’t want to post it yet.

### Adjectives

The four particles representing the degrees _most_ (superlative), _more_ (comparative), _less_ (negative comparative), and _least_ (negative superlative) are _néa_, _nus_, _séa_, and _sun_ respectively. They follow their adjectives, e.g. _gí_ (_happy_) and _gí néa_ (_happiest_).

### Thoughs and Stuff

I’ve been thinking that I might make it a common idiom in the language that stuff like adjectives of colour would be simply nouns in the genitive case. But what about the comparitives? Hmmm...

Similarly, I’ve been thinking of using the genitive plural with counted nouns, e.g. five apples = five of apples, or something similar. That seems pretty neat, and it’s make the language looks somewhat cleaner to boot.
