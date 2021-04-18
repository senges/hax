# Hax
## Install

To start using hax, it is recommanded to run `hax config` in the first place.

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

**run**

If you just want to run default image, `hax` command alone is enough !

```
➜  hax run <image>
```

Hax images are :

* hax (default)
* msf
* minimal
* cracking
* osing
* expose (for the expose command)

**list**

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

**expose**

Expose local port using ngrok.  
For example, to expose a local mysql database :

```
➜  hax expose 3306
```

**refresh**

Pull latest version of local images only.

## Other features

* List installed tools in the docker : `tools`

## Create your own !

```
FROM hax:legacy

# Install any tool from scripts folder
RUN /install.sh any

ENTRYPOINT /some/bin
```