# Hax

Manage your CTF environment using docker images.

## Install

> I'm working on releasing a pip package to simplify hax install.

**Requirements :**

* python3
* pip
* docker

```
➜  git clone --depth 1 https://github.com/senges/hax.git /opt/hax
➜  pip install --user -r /opt/hax/requirements.txt
➜  ln -s /opt/hax/hax.py /usr/local/sbin/hax
```

To start using hax, it is recommanded to run `hax config` in the first place.  
You will be asked a few questions such as your ngrok token (for expose feature), and optionnal custom volumes, env vars.

```
➜  hax config
```

Default config include :

* Volume : `/tmp:/tmp` (read-write)
* Volume : `$HOME/.ssh:/root/.ssh` (read-only)
* Env : `NGROK_TOK`

## Usage

```bash
➜  hax -h
Usage: hax [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  config    Configure hax
  expose    Expose TCP endpoint using ngrok
  list      List local images
  pull      Pull image and exit
  refresh   Pull latest version of local images
  run       Run ctf environment
  build     Build images from source    # Not yet implemented
  wordlist  Manage wordlists            # Not yet implemented
```

**# run**

If you just want to run default image, `hax` command alone is enough !

```
➜  hax run <image>
```


| Tools            | hax | cracking | msf | expose |
|------------------|:---:|:--------:|:---:|:------:|
| arjun            |  ✓  |          |     |        |
| assetfinder      |  ✓  |          |     |        |
| cupp             |     |    ✓     |     |        |
| dirsearch        |  ✓  |          |     |        |
| exiftool         |  ✓  |          |     |        |
| fcrackzip        |     |    ✓     |     |        |
| ffuf             |  ✓  |          |     |        |
| foremost         |  ✓  |          |     |        |
| hashcat          |     |    ✓     |     |        |
| john             |  ✓  |    ✓     |  ✓  |        |
| metasploit       |     |          |     |        |
| mysql            |  ✓  |          |     |        |
| ngrok            |     |          |     |   ✓    |
| nikto            |  ✓  |          |     |        |
| nmap             |  ✓  |          |     |        |
| php              |  ✓  |          |     |        |
| pydictor         |     |    ✓     |     |        |
| python3          |  ✓  |    ✓     |     |        |
| samdump2         |     |    ✓     |     |        |
| searchsploit.min |  ✓  |          |     |        |
| sherlock         |  ✓  |          |     |        |
| sqlmap           |  ✓  |          |     |        |
| zsh              |  ✓  |    ✓     |     |        |

> Legacy image is just top layer image and is not aimed to be run by its own

**# list**

List local hax images.

```
➜  hax list
┌──────────┬────────┬───────┐
│ Images   │   Size │ State │
├──────────┼────────┼───────┤
│ legacy   │ 279 Mo │   ✓   │
│ hax      │ 485 Mo │   ✓   │
│ minimal  │      - │   ✗   │
│ expose   │  30 Mo │   ✓   │
│ msf      │      - │   ✗   │
│ cracking │      - │   ✗   │
│ osint    │      - │   ✗   │
└──────────┴────────┴───────┘
```

**# expose**

Expose local port using ngrok.  
For example, to expose a local mysql database :

```
➜  hax expose 3306
```

**# pull**

Pull one image from above.

```
➜  hax pull msf
~ Pulling image hax:msf from registry
✓ Image hax:msf pull done
```

**# refresh**

Pull latest version of local images only.

## Other features

* List installed tools in the docker : `tools`
* Add custom volumes / env vars is config file using `hax config`

## Create your own !

```
FROM hax:legacy

# Install any tool from scripts folder
RUN /install.sh any

ENTRYPOINT /some/bin
```