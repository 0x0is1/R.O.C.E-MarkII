# ROCE -MarkII

## Description

Roce is a discord bots series of unique bots, this version is mark 2, which is used to connect ncbi cli API embedded in discord.py for genetical engineerng and research purpose with some easter eggs features.

This tool is based on our previous developed cli tool for ncbi data access [glimmer](https://github.com/0x0is1/glimmer.git). glimmer is a tool which do not really uses ncbi data api but, it uses it's scrapping feature to get data from rendered webpages from [ncbi's official website](https://www.ncbi.nlm.nih.gov).

## Install

You can use [this](https://discord.com/oauth2/authorize?client_id=798966300448784425&permissions=8&scope=bot
) invite link to call this bot on your server, if you are genetic engineering or student, it is available for public usage.

## Host

You can also host this bot by using following processes:

* Download this repository directly or by using git cli i.e-

```css
> git clone https://github.com/0x0is1/R.O.C.E-MarkII
> python3 -m pip install requirements.txt
> export EXPERIMENTAL_BOT_TOKEN='<Your bot token here>'
> python3 mark2.py
```

## Requirements

* Python3.5+
* python-requests
* discord.py
* Beautifulsoup (bs4)
* urllib

## Compatibilty _(for hosting this bot personally)_

Any device that can run discord bots including raspberry pi and other OS'es.

## Commands

* `set` : Command used for seting parameters to get data.
* `get` : Command used for getting parameter.
* `search`: command used to make search for genetic materials.
* `option`: command used for getting options saved.

Type help <COMMAND_NAME> to get help for specific command.

## Sub-commands

**set:**

* `Description`: used for setting item id and item type.
* `Example`: set id 1798174254 and set type nuccore
* `Options for item type`:
  * _Nucleotide (nuccore)_
  * _Genes (gene)_
  * _Protein (protein)_
  * _Probe (probe)_
  * _Popset(popset)_

`Options for item id:` use search <ITEM_TYPE> <ITEM_NAME> to get `ids`.

**get:**

* `Description`:
use for getting data for saved item id and item type.
* `Example`:
get gene, get cds etc.
* `Options for get`:
  * _Name (name)_
  * _Overview (overview)_
  * _Comments (comment)_
  * _Gene (gene)_
  * _Stem Loop (stem-loop)_
  * _Peptide (peptide)_
  * _CDS (cds)_
  * _Source (source)_
  * _All(soup)_

**search:**

* `Description`:
use for searching data for specific detail type.
* `Example`:
search nuccore SARS, search gene rept etc.
* `Options for item type`:
  * _Nucleotide (nuccore)_
  * _Genes (gene)_
  * _Protein (protein)_
  * _Probe (probe)_
  * _Popset(popset)_

## Feedback and bug report

Send feedback or bug report to our developers on this [mail id](0x0is1@protonmail.com).

## Previews

![peview-1](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/p1.png)

![peview-2](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/p2.png)

![peview-3](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/p3.png)
