#
# This program requires installation of the splinter
# library.  See: http://splinter.cobrateam.info/
#

from splinter import Browser
import json, getopt
import sys
import time

test_config = None


def usage(argv):
    print "Usage:"
    print "    %s -f [JSON config file]" % argv[0]


# The following test opens a web browser.
#   (1) opens a web browser
#   (2) clicks on the System icon
#   (3) clicks on the Services icon
#   (4) clicks on the SSH settings to enable ssh, and permit ssh root login
#   (5) set the admin password

def main(argv):

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:")
    except getopt.GetoptError as err:
        sys.exit(2)

    global test_config
    config_file_name = None

    for o, a in opts:
        if o == "-f":
            config_file_name = a
        else:
            assert False, "unhandled option"

    if config_file_name is None:
        usage(argv)
        sys.exit(1)

    config_file = open(config_file_name, "r")
    test_config = json.load(config_file)

    browser = Browser()
    browser.visit(test_config['url'])

    # log in
    browser.find_by_id('id_username').fill(test_config['username'])
    browser.find_by_id('id_password').fill(test_config['password'])
    browser.find_by_id('dijit_form_Button_0_label').click()

    # Enable SSH
    browser.find_by_id('menuBar_System').click()
    browser.find_by_id('menuBar_Services').click()
    browser.find_by_id('ssh_settings').click()
    browser.find_by_id('id_ssh_rootlogin').check()
    browser.find_by_id('btn_SSH_Ok_label').click()
    browser.find_by_id('ssh_toggle').check()

    browser.quit()

    print "\nn\=========================================="
    print "SSH access enabled for: "+test_config['ip']
    print "==========================================\n\n"


if __name__ == "__main__":
    main(sys.argv)
