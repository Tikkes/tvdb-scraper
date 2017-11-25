""" Script to scrape TV show meta data from TVDB and creates XML files for each
season and episode. """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import sys
import tvdb_api

from absl import flags
# from absl import logging

FLAGS = flags.FLAGS

flags.DEFINE_string('series', None, 'series to look up')

BASE_URL = 'https://raw.githubusercontent.com/Tikkes/darkside-repo/master/xml/'

# FULLTITLE = ""
# IMDBID = ""
# tvdbId = ""
# tvShowTitle = ""
# year = ""
# episodeName = ""
# premiered = ""
# seasonNumber = ""
# episodeNumber = ""

# show = ""
# season = ""
# episode = ""


def main(argv):
    """ Main function. """
    argv = FLAGS(argv)

    tvdb = tvdb_api.Tvdb()
    try:
        show = tvdb[FLAGS.series]
    except tvdb_api.tvdb_shownotfound:
        print("TV Show not found!")
        return

    XML_SEASON = """
    ################################################################################
    <poster>Tikkes</poster>
    <thumbnail></thumbnail>
    <fanart></fanart>
    ################################################################################
    """

    XML_SEASON_BODY = """
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
        <link>""" + BASE_URL + """%(tvShowTitleURL)s/%(seasonFileName)s.xml</link>
        <animated_thumbnail></animated_thumbnail>
        <thumbnail></thumbnail>
        <animated_fanart></animated_fanart>
        <fanart></fanart>
    </dir>"""

    XML_EPISODE = """
    ################################################################################
    <poster>Tikkes</poster>
    <cache>10800</poster>
    <thumbnail></thumbnail>
    <fanart></fanart>
    ################################################################################
    """

    XML_EPISODE_BODY = """
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

    for season_num in show:
        season = show[season_num]

        tvdb_id = str(show['id'])
        imdb_id = show['imdbId'].encode('utf-8')
        season_name = (
            show['seriesname'].encode('utf-8') + " Season " + str(season_num))
        tv_show_title = show['seriesname'].encode('utf-8')
        year = show['firstAired'][0:4].encode('utf-8')
        season_number = str(season_num)
        season_filename = re.sub('\W+', '',
                                 show['seriesname']) + str(season_num).zfill(2)

        SeasonData = {
            'seasonName': season_name,
            'imdbId': imdb_id,
            'tvdbId': tvdb_id,
            'tvShowTitle': tv_show_title,
            'tvShowTitleURL': re.sub('\W+', '', tv_show_title),
            'year': year,
            'seasonNumber': season_number,
            'seasonFileName': season_filename
        }
        XML_SEASON += XML_SEASON_BODY % SeasonData

        for episode_num in season:
            episode = season[episode_num]
            if not episode['episodename']:
                episodename = "N/A"
            else:
                episodename = episode['episodename']

            full_title = show['seriesname'].encode('utf-8') + " S" + str(
                season_num) + "E" + str(
                    episode_num) + " - " + episodename.encode('utf-8')
            episode_year = episode['firstAired'][0:4].encode('utf-8')
            episode_name = episodename.encode('utf-8')
            premiered = episode['firstAired'].encode('utf-8')
            episode_number = str(episode_num)

            data = {
                'fullTitle': full_title,
                'imdbId': imdb_id,
                'tvdbId': tvdb_id,
                'tvShowTitle': tv_show_title,
                'year': episode_year,
                'episodeName': episode_name,
                'premiered': premiered,
                'seasonNumber': season_number,
                'episodeNumber': episode_number
            }

            XML_EPISODE += XML_EPISODE_BODY % data

        current_directory = os.getcwd()
        xml_directory = os.path.join(current_directory, r'xml')
        if not os.path.exists(xml_directory):
            os.makedirs(xml_directory)

        show_directory = re.sub('\W+', '', show['seriesname'])
        xml2_directory = os.path.join(current_directory, xml_directory)
        final_directory = os.path.join(xml2_directory, show_directory)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        save_path_file = (
            'xml\\' + show_directory + '\\' + show_directory + '.xml')
        with open(save_path_file, 'w') as xml_file:
            xml_file.write(XML_SEASON)

        save_path_file = ('xml\\' + show_directory + '\\' + show_directory +
                          str(season_num).zfill(2) + '.xml')
        with open(save_path_file, 'w') as xml_file:
            xml_file.write(XML_EPISODE)
    print("XML files written to " + final_directory)


if __name__ == '__main__':
    main(sys.argv)
