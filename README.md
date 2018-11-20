![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)

# ospd-ssh-keyscan

This is an OSP server implementation to allow GVM to remotely control
the `ssh-keyscan` tool of OpenSSH, see <https://man.openbsd.org/ssh-keyscan.1>.

Once running, you need to configure the Scanner for Greenbone Vulnerability
Manager, for example via the web interface Greenbone Security Assistant.
Then you can create scan tasks to use this scanner.

## Installation

### Requirements

Python 3 and later is supported.

Beyond the [ospd base library](https://github.com/greenbone/ospd) and the
`ssh-keyscan` tool, `ospd-ssh-keyscan` has no further dependecies.

There are no special installation aspects for this module beyond the general
installation guide for ospd-based scanners.

Please follow the general installation guide for ospd-based scanners:

  <https://github.com/greenbone/ospd/blob/master/doc/INSTALL-ospd-scanner>

## Usage

There are no special usage aspects for this module beyond the generic usage
guide.

Please follow the general usage guide for ospd-based scanners:

  <https://github.com/greenbone/ospd/blob/master/doc/USAGE-ospd-scanner>

## Support

For any question on the usage of ospd-ssh-keyscan please use the [Greenbone
Community Portal](https://community.greenbone.net/c/gse). If you found a
problem with the software, please [create an
issue](https://github.com/greenbone/ospd-ssh-keyscan/issues) on GitHub. If you
are a Greenbone customer you may alternatively or additionally forward your
issue to the Greenbone Support Portal.

## Maintainer

This project is maintained by [Greenbone Networks
GmbH](https://www.greenbone.net/).

## Contributing

Your contributions are highly appreciated. Please [create a pull
request](https://github.com/greenbone/ospd-ssh-keyscan/pulls) on GitHub. Bigger
changes need to be discussed with the development team via the [issues section
at GitHub](https://github.com/greenbone/ospd-ssh-keyscan/issues) first.

## License

Copyright (C) 2015-2018 [Greenbone Networks GmbH](https://www.greenbone.net/)

Licensed under the [GNU General Public License v2.0 or later](COPYING).
