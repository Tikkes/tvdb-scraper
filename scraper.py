""" Script to scrape TV show meta data from TVDB and creates XML files for each
season and episode. """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import errno
import os
import pdb
import sys
import traceback
import tvdb_api

from absl import app
from absl import command_name
from absl import flags
from absl import logging
from xml.dom import minidom

FLAGS = flags.FLAGS

flags.DEFINE_string('series', None, 'series to look up')

GIT_PATH = 'https://raw.githubusercontent.com/Tikkes/darkside-repo/master/xml/'

fullTitle = ""
imdbId = ""
tvdbId = ""
tvShowTitle = ""
year = ""
episodeName = ""
premiered = ""
seasonNumber = ""
episodeNumber = ""

show = ""
season = ""
episode = ""


def main(argv):
    argv = FLAGS(argv)

    t = tvdb_api.Tvdb()
    try:
        show = t[FLAGS.series]
    except(tvdb_api.tvdb_shownotfound):
        print("TV Show not found!")
        return

    xmlSeriesTemplate = """
################################################################################
<poster>Tikkes</poster>
<thumbnail></thumbnail>
<fanart></fanart>
################################################################################
"""

    xmlSeriesTemplateBody = """
<dir>
    <name>%(seasonName)s</name>
    <meta>
        <content>season</content>
        <imdb>%(imdbId)s</imdb>
        <tvdb>%(tvdbId)s</tvdb>
        <tvshowtitle>%(tvShowTitle)s</tvshowtitle>
        <year>%(year)s</year>
        <season>%(seasonNumber)s</season>
    </meta>
    <link>""" + GIT_PATH + """%(seasonFileName)s.xml</link>
    <animated_thumbnail></animated_thumbnail>
    <thumbnail></thumbnail>
    <animated_fanart></animated_fanart>
    <fanart></fanart>
</dir>"""

    xmlTemplateBody = """
<item>
    <title>%(fullTitle)s</title>
    <meta>
        <content>episode</content>
        <imdb>%(imdbId)s</imdb>
        <tvdb>%(tvdbId)s</tvdb>
        <tvshowtitle>%(tvShowTitle)s</tvshowtitle>
        <year>%(year)s</year>
        <title>%(episodeName)s</title>
        <premiered>%(premiered)s</premiered>
        <season>%(seasonNumber)s</season>
        <episode>%(episodeNumber)s</episode>
    </meta>
    <link>
        <sublink>search</sublink>
        <sublink>searchsd</sublink>
    </link>
    <animated_thumbnail></animated_thumbnail>
    <thumbnail></thumbnail>
    <animated_fanart></animated_fanart>
    <fanart></fanart>
</item>"""

    for s in show:
        season = show[s]
        xmlTemplate = """
################################################################################
<poster>Tikkes</poster>
<cache>10800</poster>
<thumbnail></thumbnail>
<fanart></fanart>
################################################################################
"""
        seasonData = {
            'seasonName':
            (show['seriesname'].encode('utf-8') + " Season " + str(s)),
            'imdbId':
            show['imdbId'].encode('utf-8'),
            'tvdbId':
            str(show['id']),
            'tvShowTitle':
            show['seriesname'].encode('utf-8'),
            'year':
            show['firstAired'][0:4].encode('utf-8'),
            'seasonNumber':
            str(s),
            'seasonFileName':
            show['seriesname'].encode('utf-8').replace(" ", "") +
            str(s).zfill(2)
        }
        xmlSeriesTemplate += xmlSeriesTemplateBody % seasonData

        for e in season:
            episode = season[e]
            if not episode['episodename']:
                episodename = "N/A"
            else:
                episodename = episode['episodename']

            data = {
                'fullTitle':
                show['seriesname'].encode('utf-8') + ' S' + str(s).zfill(2) +
                'E' + str(e).zfill(2) + ' - ' + episodename.encode('utf-8'),
                'imdbId':
                show['imdbId'].encode('utf-8'),
                'tvdbId':
                str(show['id']),
                'tvShowTitle':
                show['seriesname'].encode('utf-8'),
                'year':
                episode['firstAired'][0:4].encode('utf-8'),
                'episodeName':
                episodename.encode('utf-8'),
                'premiered':
                episode['firstAired'].encode('utf-8'),
                'seasonNumber':
                str(s),
                'episodeNumber':
                str(e)
            }
            fullTitle = show['seriesname'].encode('utf-8') + " S" + str(
                s) + "E" + str(e) + " - " + episodename.encode('utf-8')
            imdbId = show['imdbId'].encode('utf-8')
            tvdbId = str(show['id'])
            tvShowTitle = show['seriesname'].encode('utf-8')
            year = episode['firstAired'][0:4].encode('utf-8')
            episodeName = episodename.encode('utf-8')
            premiered = episode['firstAired'].encode('utf-8')
            seasonNumber = str(s)
            episodeNumber = str(e)
            xmlTemplate += xmlTemplateBody % data

        current_directory = os.getcwd()
        xml_directory = os.path.join(current_directory, r'xml')
        if not os.path.exists(xml_directory):
            os.makedirs(xml_directory)

        show_directory = show['seriesname']
        xml2_directory = os.path.join(current_directory, xml_directory)
        final_directory = os.path.join(xml2_directory, show_directory)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        save_path_file = 'xml\\' + show['seriesname'] + '\\' + \
            show['seriesname'].encode('utf-8').replace(" ", "") + '.xml'
        with open(save_path_file, 'w') as f:
            f.write(xmlSeriesTemplate)

        save_path_file = ('xml\\' + show['seriesname'] + '\\' +
                          show['seriesname'].encode('utf-8').replace(" ", "") +
                          str(s).zfill(2) + '.xml')
        with open(save_path_file, 'w') as f:
            f.write(xmlTemplate)
    print("XML files written to " + final_directory)

if __name__ == '__main__':
    main(sys.argv)
