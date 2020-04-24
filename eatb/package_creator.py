""" Command line utility for creating E-ARK Submission and Archival IPs. """
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import uuid
import logging

from eatb.oais.aip_creation import create_aip
from eatb.oais.sip_creation import create_sip
from eatb.oais.oais_package_type import OAISPackageType

LOGGER = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(description='eArchiving Toolbox - command line interface (CLI).')

    parser.add_argument('--name', "-n", type=str, help='Information package name', required=True)
    parser.add_argument('--directory', "-d", type=str, help='Information package content directory', required=True)
    parser.add_argument('--premis', "-p", action='store_true', help='Generate premis skeleton')
    parser.add_argument('--type', "-t", type=str, default="SIP",
                        choices=["SIP", "AIP"], help="Package type")
    parser.add_argument('--identifier', "-i", default=uuid.uuid4().__str__(), help='Identifier (default: generated)')
    parser.add_argument('--package', "-c", action='store_true', help='Create TAR package', default=True)
    args = parser.parse_args()

    if not os.path.exists(args.directory):
        msg = "The directory does not exist: %s" % args.directory
        LOGGER.error(msg)
        raise FileNotFoundError(msg)

    if OAISPackageType[args.type] == OAISPackageType.SIP and create_sip(args.directory, args.name, args.identifier):
        LOGGER.info("SIP created successfully")
    elif OAISPackageType[args.type] == OAISPackageType.AIP and create_aip(args.directory, args.name, args.identifier):
        LOGGER.info("AIP created successfully")
    else:
        LOGGER.error("Package type not supported")


if __name__ == '__main__':
    main()
