#!/usr/bin/env python3
"""
FULL DIOCESE EMAIL HARVESTER
Derives emails from known diocese website domains
"""

import json
import re
from urllib.parse import urlparse

# All US Dioceses with websites (from USCCB)
DIOCESES = [
    # ALABAMA
    {"name": "Archdiocese of Mobile", "address": "400 Government Street, Mobile, AL 36602", "website": "mobarch.org"},
    {"name": "Diocese of Birmingham", "address": "2121 3rd Avenue North, Birmingham, AL 35202", "website": "bhmdiocese.org"},

    # ALASKA
    {"name": "Archdiocese of Anchorage-Juneau", "address": "225 Cordova Street, Anchorage, AK 99501", "website": "aoaj.org"},
    {"name": "Diocese of Fairbanks", "address": "1316 Peger Road, Fairbanks, AK 99709", "website": "dioceseoffairbanks.org"},

    # ARIZONA
    {"name": "Diocese of Phoenix", "address": "400 East Monroe Street, Phoenix, AZ 85004", "website": "diocesephoenix.org"},
    {"name": "Diocese of Tucson", "address": "P.O. Box 31, Tucson, AZ 85702", "website": "diocesetucson.org"},

    # ARKANSAS
    {"name": "Diocese of Little Rock", "address": "2500 N. Tyler Street, Little Rock, AR 72207", "website": "dolr.org"},

    # CALIFORNIA
    {"name": "Archdiocese of Los Angeles", "address": "3424 Wilshire Boulevard, Los Angeles, CA 90010", "website": "lacatholics.org"},
    {"name": "Archdiocese of San Francisco", "address": "One Peter Yorke Way, San Francisco, CA 94109", "website": "sfarchdiocese.org"},
    {"name": "Diocese of Fresno", "address": "1550 North Fresno Street, Fresno, CA 93707", "website": "dioceseoffresno.org"},
    {"name": "Diocese of Monterey", "address": "425 Church Street, Monterey, CA 93940", "website": "dioceseofmonterey.org"},
    {"name": "Diocese of Oakland", "address": "2121 Harrison Street, Oakland, CA 94612", "website": "oakdiocese.org"},
    {"name": "Diocese of Orange", "address": "13280 Chapman Avenue, Garden Grove, CA 92840", "website": "rcbo.org"},
    {"name": "Diocese of Sacramento", "address": "2110 Broadway, Sacramento, CA 95818", "website": "scd.org"},
    {"name": "Diocese of San Bernardino", "address": "1201 E. Highland Avenue, San Bernardino, CA 92404", "website": "sbdiocese.org"},
    {"name": "Diocese of San Diego", "address": "P.O. Box 85728, San Diego, CA 92186", "website": "sdcatholic.org"},
    {"name": "Diocese of San Jose", "address": "1150 North 1st Street, San Jose, CA 95112", "website": "dsj.org"},
    {"name": "Diocese of Santa Rosa", "address": "P.O. Box 1297, Santa Rosa, CA 95402", "website": "srdiocese.org"},
    {"name": "Diocese of Stockton", "address": "212 N. San Joaquin Street, Stockton, CA 95202", "website": "stocktondiocese.org"},

    # COLORADO
    {"name": "Archdiocese of Denver", "address": "1300 South Steele Street, Denver, CO 80210", "website": "archden.org"},
    {"name": "Diocese of Colorado Springs", "address": "228 N. Cascade Avenue, Colorado Springs, CO 80903", "website": "diocs.org"},
    {"name": "Diocese of Pueblo", "address": "101 N. Greenwood Street, Pueblo, CO 81003", "website": "dioceseofpueblo.org"},

    # CONNECTICUT
    {"name": "Archdiocese of Hartford", "address": "467 Bloomfield Avenue, Bloomfield, CT 06002", "website": "archdioceseofhartford.org"},
    {"name": "Diocese of Bridgeport", "address": "100 Beard Sawmill Road, Shelton, CT 06848", "website": "bridgeportdiocese.com"},
    {"name": "Diocese of Norwich", "address": "201 Broadway, Norwich, CT 06360", "website": "norwichdiocese.org"},

    # DELAWARE
    {"name": "Diocese of Wilmington", "address": "1925 Delaware Avenue, Wilmington, DE 19899", "website": "cdow.org"},

    # FLORIDA
    {"name": "Archdiocese of Miami", "address": "9401 Biscayne Boulevard, Miami Shores, FL 33138", "website": "miamiarch.org"},
    {"name": "Diocese of Orlando", "address": "P.O. Box 1800, Orlando, FL 32802", "website": "orlandodiocese.org"},
    {"name": "Diocese of Palm Beach", "address": "9995 N. Military Trail, Palm Beach Gardens, FL 33410", "website": "diocesepb.org"},
    {"name": "Diocese of Pensacola-Tallahassee", "address": "11 North B Street, Pensacola, FL 32502", "website": "ptdiocese.org"},
    {"name": "Diocese of St. Augustine", "address": "11625 Old St. Augustine Rd., Jacksonville, FL 32258", "website": "dosafl.com"},
    {"name": "Diocese of St. Petersburg", "address": "6363 9th Avenue N., St. Petersburg, FL 33710", "website": "dosp.org"},
    {"name": "Diocese of Venice", "address": "1000 Pinebrook Road, Venice, FL 34285", "website": "dioceseofvenice.org"},

    # GEORGIA
    {"name": "Archdiocese of Atlanta", "address": "2401 Lake Park Drive, S.E., Smyrna, GA 30080", "website": "archatl.com"},
    {"name": "Diocese of Savannah", "address": "2170 East Victory Drive, Savannah, GA 31404", "website": "diosav.org"},

    # HAWAII
    {"name": "Diocese of Honolulu", "address": "1184 Bishop Street, Honolulu, HI 96813", "website": "catholichawaii.org"},

    # IDAHO
    {"name": "Diocese of Boise", "address": "1501 S. Federal Way, Boise, ID 83705", "website": "catholicidaho.org"},

    # ILLINOIS
    {"name": "Archdiocese of Chicago", "address": "835 N. Rush Street, Chicago, IL 60611", "website": "archchicago.org"},
    {"name": "Diocese of Belleville", "address": "222 South Third Street, Belleville, IL 62220", "website": "diobelle.org"},
    {"name": "Diocese of Joliet", "address": "16555 Weber Road, Crest Hill, IL 60403", "website": "dioceseofjoliet.org"},
    {"name": "Diocese of Peoria", "address": "419 N.E. Madison Avenue, Peoria, IL 61603", "website": "cdop.org"},
    {"name": "Diocese of Rockford", "address": "555 Coleman Center Drive, Rockford, IL 61108", "website": "rockforddiocese.org"},
    {"name": "Diocese of Springfield in Illinois", "address": "1615 West Washington Street, Springfield, IL 62702", "website": "dio.org"},

    # INDIANA
    {"name": "Archdiocese of Indianapolis", "address": "1400 N. Meridian Street, Indianapolis, IN 46202", "website": "archindy.org"},
    {"name": "Diocese of Evansville", "address": "4200 N. Kentucky Avenue, Evansville, IN 47724", "website": "evdio.org"},
    {"name": "Diocese of Fort Wayne-South Bend", "address": "915 South Clinton, Fort Wayne, IN 46801", "website": "diocesefwsb.org"},
    {"name": "Diocese of Gary", "address": "9292 Broadway, Merrillville, IN 46410", "website": "dcgary.org"},
    {"name": "Diocese of Lafayette in Indiana", "address": "P.O. Box 260, Lafayette, IN 47902", "website": "dol-in.org"},

    # IOWA
    {"name": "Archdiocese of Dubuque", "address": "1229 Mt. Loretta Avenue, Dubuque, IA 52003", "website": "dbqarch.org"},
    {"name": "Diocese of Davenport", "address": "780 W. Central Park Av., Davenport, IA 52804", "website": "davenportdiocese.org"},
    {"name": "Diocese of Des Moines", "address": "601 Grand Avenue, Des Moines, IA 50309", "website": "dmdiocese.org"},
    {"name": "Diocese of Sioux City", "address": "1821 Jackson Street, Sioux City, IA 51102", "website": "scdiocese.org"},

    # KANSAS
    {"name": "Archdiocese of Kansas City in Kansas", "address": "12615 Parallel Parkway, Kansas City, KS 66109", "website": "archkck.org"},
    {"name": "Diocese of Dodge City", "address": "P.O. Box 137, Dodge City, KS 67801", "website": "dcdiocese.org"},
    {"name": "Diocese of Salina", "address": "103 North Ninth Street, Salina, KS 67401", "website": "salinadiocese.org"},
    {"name": "Diocese of Wichita", "address": "424 N. Broadway, Wichita, KS 67202", "website": "catholicdioceseofwichita.org"},

    # KENTUCKY
    {"name": "Archdiocese of Louisville", "address": "3940 Poplar Level Road, Louisville, KY 40213", "website": "archlou.org"},
    {"name": "Diocese of Covington", "address": "1125 Madison Avenue, Covington, KY 41011", "website": "covingtondiocese.org"},
    {"name": "Diocese of Lexington", "address": "1310 W. Main Street, Lexington, KY 40508", "website": "cdlex.org"},
    {"name": "Diocese of Owensboro", "address": "600 Locust Street, Owensboro, KY 42301", "website": "rcdok.org"},

    # LOUISIANA
    {"name": "Archdiocese of New Orleans", "address": "7887 Walmsley Avenue, New Orleans, LA 70125", "website": "arch-no.org"},
    {"name": "Diocese of Alexandria", "address": "4400 Coliseum Boulevard, Alexandria, LA 71303", "website": "diocesealex.org"},
    {"name": "Diocese of Baton Rouge", "address": "P.O. Box 2028, Baton Rouge, LA 70821", "website": "diobr.org"},
    {"name": "Diocese of Houma-Thibodaux", "address": "2779 Highway 311, Schriever, LA 70395", "website": "htdiocese.org"},
    {"name": "Diocese of Lafayette in Louisiana", "address": "1408 Carmel Drive, Lafayette, LA 70501", "website": "diolaf.org"},
    {"name": "Diocese of Lake Charles", "address": "414 Iris Street, Lake Charles, LA 70601", "website": "lcdiocese.org"},
    {"name": "Diocese of Shreveport", "address": "3500 Fairfield Avenue, Shreveport, LA 71104", "website": "dioshpt.org"},

    # MAINE
    {"name": "Diocese of Portland in Maine", "address": "510 Ocean Avenue, Portland, ME 04103", "website": "portlanddiocese.net"},

    # MARYLAND
    {"name": "Archdiocese of Baltimore", "address": "320 Cathedral Street, Baltimore, MD 21201", "website": "archbalt.org"},

    # MASSACHUSETTS
    {"name": "Archdiocese of Boston", "address": "66 Brooks Drive, Braintree, MA 02184", "website": "bostoncatholic.org"},
    {"name": "Diocese of Fall River", "address": "450 Highland Avenue, Fall River, MA 02720", "website": "fallriverdiocese.org"},
    {"name": "Diocese of Springfield MA", "address": "P.O. Box 1730, Springfield, MA 01102", "website": "diospringfield.org"},
    {"name": "Diocese of Worcester", "address": "49 Elm Street, Worcester, MA 01609", "website": "worcesterdiocese.org"},

    # MICHIGAN
    {"name": "Archdiocese of Detroit", "address": "12 State Street, Detroit, MI 48226", "website": "aod.org"},
    {"name": "Diocese of Gaylord", "address": "611 W. North Street, Gaylord, MI 49735", "website": "dioceseofgaylord.org"},
    {"name": "Diocese of Grand Rapids", "address": "360 Division Avenue S., Grand Rapids, MI 49503", "website": "grdiocese.org"},
    {"name": "Diocese of Kalamazoo", "address": "215 N. Westnedge Avenue, Kalamazoo, MI 49007", "website": "dioceseofkalamazoo.org"},
    {"name": "Diocese of Lansing", "address": "228 N. Walnut Street, Lansing, MI 48933", "website": "dioceseoflansing.org"},
    {"name": "Diocese of Marquette", "address": "1004 Harbor Hills Drive, Marquette, MI 49855", "website": "dioceseofmarquette.org"},
    {"name": "Diocese of Saginaw", "address": "5800 Weiss Street, Saginaw, MI 48603", "website": "saginaw.org"},

    # MINNESOTA
    {"name": "Archdiocese of St. Paul and Minneapolis", "address": "777 Forest Street, Saint Paul, MN 55106", "website": "archspm.org"},
    {"name": "Diocese of Crookston", "address": "620 Summit Avenue N., Crookston, MN 56716", "website": "crookston.org"},
    {"name": "Diocese of Duluth", "address": "2830 E. Fourth Street, Duluth, MN 55812", "website": "dioceseduluth.org"},
    {"name": "Diocese of New Ulm", "address": "1400 6th Street North, New Ulm, MN 56073", "website": "dnu.org"},
    {"name": "Diocese of St. Cloud", "address": "P.O. Box 1248, St. Cloud, MN 56302", "website": "stcdio.org"},
    {"name": "Diocese of Winona-Rochester", "address": "55 W. Sanborn, Winona, MN 55987", "website": "dow.org"},

    # MISSISSIPPI
    {"name": "Diocese of Biloxi", "address": "1790 Popps Ferry Road, Biloxi, MS 39532", "website": "biloxidiocese.org"},
    {"name": "Diocese of Jackson", "address": "237 East Amite, Jackson, MS 39225", "website": "jacksondiocese.org"},

    # MISSOURI
    {"name": "Archdiocese of St. Louis", "address": "20 Archbishop May Drive, St. Louis, MO 63119", "website": "archstl.org"},
    {"name": "Diocese of Jefferson City", "address": "2207 West Main Street, Jefferson City, MO 65110", "website": "diojeffcity.org"},
    {"name": "Diocese of Kansas City-St. Joseph", "address": "P.O. Box 419037, Kansas City, MO 64141", "website": "kcsjcatholic.org"},
    {"name": "Diocese of Springfield-Cape Girardeau", "address": "601 S. Jefferson Avenue, Springfield, MO 65806", "website": "dioscg.org"},

    # MONTANA
    {"name": "Diocese of Great Falls-Billings", "address": "P.O. Box 1399, Great Falls, MT 59403", "website": "diocesegfb.org"},
    {"name": "Diocese of Helena", "address": "P.O. Box 1729, Helena, MT 59624", "website": "diocesehelena.org"},

    # NEBRASKA
    {"name": "Archdiocese of Omaha", "address": "2222 N. 111th Street, Omaha, NE 68164", "website": "archomaha.org"},
    {"name": "Diocese of Grand Island", "address": "2708 Old Fair Road, Grand Island, NE 68803", "website": "gidiocese.org"},
    {"name": "Diocese of Lincoln", "address": "3400 Sheridan Boulevard, Lincoln, NE 68506", "website": "dioceseoflincoln.org"},

    # NEVADA
    {"name": "Archdiocese of Las Vegas", "address": "336 Cathedral Way, Las Vegas, NV 89109", "website": "lvcatholic.org"},
    {"name": "Diocese of Reno", "address": "290 S. Arlington Avenue, Reno, NV 89501", "website": "dioceseofreno.org"},

    # NEW HAMPSHIRE
    {"name": "Diocese of Manchester", "address": "153 Ash Street, Manchester, NH 03104", "website": "catholicnh.org"},

    # NEW JERSEY
    {"name": "Archdiocese of Newark", "address": "171 Clifton Avenue, Newark, NJ 07104", "website": "rcan.org"},
    {"name": "Diocese of Camden", "address": "631 Market Street, Camden, NJ 08102", "website": "camdendiocese.org"},
    {"name": "Diocese of Metuchen", "address": "P.O. Box 191, Metuchen, NJ 08840", "website": "diometuchen.org"},
    {"name": "Diocese of Paterson", "address": "777 Valley Road, Clifton, NJ 07013", "website": "patersondiocese.org"},
    {"name": "Diocese of Trenton", "address": "P.O. Box 5147, Trenton, NJ 08638", "website": "dioceseoftrenton.org"},

    # NEW MEXICO
    {"name": "Archdiocese of Santa Fe", "address": "4000 St. Joseph's Pl. NW, Albuquerque, NM 87120", "website": "archdiosf.org"},
    {"name": "Diocese of Gallup", "address": "P.O. Box 1338, Gallup, NM 87305", "website": "dioceseofgallup.org"},
    {"name": "Diocese of Las Cruces", "address": "1280 Med Park Drive, Las Cruces, NM 88005", "website": "rcdlc.org"},

    # NEW YORK
    {"name": "Archdiocese of New York", "address": "1011 First Avenue, New York, NY 10022", "website": "archny.org"},
    {"name": "Diocese of Albany", "address": "40 North Main Avenue, Albany, NY 12203", "website": "rcda.org"},
    {"name": "Diocese of Brooklyn", "address": "310 Prospect Park West, Brooklyn, NY 11215", "website": "dioceseofbrooklyn.org"},
    {"name": "Diocese of Buffalo", "address": "795 Main Street, Buffalo, NY 14203", "website": "buffalodiocese.org"},
    {"name": "Diocese of Ogdensburg", "address": "622 Washington Street, Ogdensburg, NY 13669", "website": "rcdony.org"},
    {"name": "Diocese of Rochester", "address": "1150 Buffalo Road, Rochester, NY 14624", "website": "dor.org"},
    {"name": "Diocese of Rockville Centre", "address": "50 North Park Avenue, Rockville Centre, NY 11571", "website": "drvc.org"},
    {"name": "Diocese of Syracuse", "address": "240 East Onondaga Street, Syracuse, NY 13201", "website": "syracusediocese.org"},

    # NORTH CAROLINA
    {"name": "Diocese of Charlotte", "address": "1123 South Church Street, Charlotte, NC 28203", "website": "charlottediocese.org"},
    {"name": "Diocese of Raleigh", "address": "7200 Stonehenge Drive, Raleigh, NC 27613", "website": "dioceseofraleigh.org"},

    # NORTH DAKOTA
    {"name": "Diocese of Bismarck", "address": "P.O. Box 1575, Bismarck, ND 58502", "website": "bismarckdiocese.com"},
    {"name": "Diocese of Fargo", "address": "5201 Bishops Boulevard, Fargo, ND 58104", "website": "fargodiocese.org"},

    # OHIO
    {"name": "Archdiocese of Cincinnati", "address": "100 East Eighth Street, Cincinnati, OH 45202", "website": "catholiccincinnati.org"},
    {"name": "Diocese of Cleveland", "address": "1404 East Ninth Street, Cleveland, OH 44114", "website": "dioceseofcleveland.org"},
    {"name": "Diocese of Columbus", "address": "197 E. Gay Street, Columbus, OH 43215", "website": "colsdioc.org"},
    {"name": "Diocese of Steubenville", "address": "422 Washington Street, Steubenville, OH 43952", "website": "diosteub.org"},
    {"name": "Diocese of Toledo", "address": "1933 Spielbusch Avenue, Toledo, OH 43604", "website": "toledodiocese.org"},
    {"name": "Diocese of Youngstown", "address": "144 W. Wood Street, Youngstown, OH 44503", "website": "doy.org"},

    # OKLAHOMA
    {"name": "Archdiocese of Oklahoma City", "address": "7501 N.W. Expressway, Oklahoma City, OK 73132", "website": "archokc.org"},
    {"name": "Diocese of Tulsa", "address": "P.O. Box 690240, Tulsa, OK 74169", "website": "dioceseoftulsa.org"},

    # OREGON
    {"name": "Archdiocese of Portland in Oregon", "address": "2838 East Burnside Street, Portland, OR 97214", "website": "archdpdx.org"},
    {"name": "Diocese of Baker", "address": "641 SW Umatilla Avenue, Redmond, OR 97756", "website": "dioceseofbaker.org"},

    # PENNSYLVANIA
    {"name": "Archdiocese of Philadelphia", "address": "222 North 17th Street, Philadelphia, PA 19103", "website": "archphila.org"},
    {"name": "Diocese of Allentown", "address": "P.O. Box F, Allentown, PA 18105", "website": "allentowndiocese.org"},
    {"name": "Diocese of Altoona-Johnstown", "address": "2713 West Chestnut Avenue, Altoona, PA 16601", "website": "ajdiocese.org"},
    {"name": "Diocese of Erie", "address": "P.O. Box 10397, Erie, PA 16514", "website": "eriercd.org"},
    {"name": "Diocese of Greensburg", "address": "723 East Pittsburgh St., Greensburg, PA 15601", "website": "dioceseofgreensburg.org"},
    {"name": "Diocese of Harrisburg", "address": "4800 Union Deposit Road, Harrisburg, PA 17111", "website": "hbgdiocese.org"},
    {"name": "Diocese of Pittsburgh", "address": "2900 Noblestown Road, Pittsburgh, PA 15205", "website": "diopitt.org"},
    {"name": "Diocese of Scranton", "address": "300 Wyoming Avenue, Scranton, PA 18503", "website": "dioceseofscranton.org"},

    # RHODE ISLAND
    {"name": "Diocese of Providence", "address": "One Cathedral Square, Providence, RI 02903", "website": "dioceseofprovidence.org"},

    # SOUTH CAROLINA
    {"name": "Diocese of Charleston", "address": "901 Orange Grove Road, Charleston, SC 29407", "website": "charlestondiocese.org"},

    # SOUTH DAKOTA
    {"name": "Diocese of Rapid City", "address": "606 Cathedral Drive, Rapid City, SD 57701", "website": "rapidcitydiocese.org"},
    {"name": "Diocese of Sioux Falls", "address": "523 N. Duluth Avenue, Sioux Falls, SD 57104", "website": "sfcatholic.org"},

    # TENNESSEE
    {"name": "Diocese of Knoxville", "address": "805 S. Northshore Drive, Knoxville, TN 37919", "website": "dioknox.org"},
    {"name": "Diocese of Memphis", "address": "5825 Shelby Oaks Drive, Memphis, TN 38134", "website": "cdom.org"},
    {"name": "Diocese of Nashville", "address": "2800 McGavock Pike, Nashville, TN 37214", "website": "dioceseofnashville.com"},

    # TEXAS
    {"name": "Archdiocese of Galveston-Houston", "address": "1700 San Jacinto, Houston, TX 77001", "website": "archgh.org"},
    {"name": "Archdiocese of San Antonio", "address": "2718 West Woodlawn Avenue, San Antonio, TX 78228", "website": "archsa.org"},
    {"name": "Diocese of Amarillo", "address": "P.O. Box 5644, Amarillo, TX 79117", "website": "amarillodiocese.org"},
    {"name": "Diocese of Austin", "address": "6225 Highway 290 East, Austin, TX 78723", "website": "austindiocese.org"},
    {"name": "Diocese of Beaumont", "address": "710 Archie Street, Beaumont, TX 77701", "website": "dioceseofbmt.org"},
    {"name": "Diocese of Brownsville", "address": "1910 University Boulevard, Brownsville, TX 78520", "website": "cdob.org"},
    {"name": "Diocese of Corpus Christi", "address": "620 Lipan Street, Corpus Christi, TX 78401", "website": "diocesecc.org"},
    {"name": "Diocese of Dallas", "address": "3725 Blackburn Street, Dallas, TX 75219", "website": "cathdal.org"},
    {"name": "Diocese of El Paso", "address": "499 St. Matthews Street, El Paso, TX 79907", "website": "elpasodiocese.org"},
    {"name": "Diocese of Fort Worth", "address": "800 West Loop 820 South, Fort Worth, TX 76108", "website": "fwdioc.org"},
    {"name": "Diocese of Laredo", "address": "1901 Corpus Christi St., Laredo, TX 78043", "website": "dioceseoflaredo.org"},
    {"name": "Diocese of Lubbock", "address": "4620 Fourth Street, Lubbock, TX 79499", "website": "catholiclubbock.org"},
    {"name": "Diocese of San Angelo", "address": "804 Ford Street, San Angelo, TX 76905", "website": "sanangelodiocese.org"},
    {"name": "Diocese of Tyler", "address": "1015 ESE Loop 323, Tyler, TX 75701", "website": "dioceseoftyler.org"},
    {"name": "Diocese of Victoria", "address": "1505 E. Mesquite Lane, Victoria, TX 77901", "website": "victoriadiocese.org"},

    # UTAH
    {"name": "Diocese of Salt Lake City", "address": "27 C Street, Salt Lake City, UT 84103", "website": "utahcatholicdiocese.org"},

    # VERMONT
    {"name": "Diocese of Burlington", "address": "55 Joy Drive, South Burlington, VT 05403", "website": "vermontcatholic.org"},

    # VIRGINIA
    {"name": "Diocese of Arlington", "address": "200 North Glebe Road, Arlington, VA 22203", "website": "arlingtondiocese.org"},
    {"name": "Diocese of Richmond", "address": "7800 Carousel Lane, Richmond, VA 23294", "website": "richmonddiocese.org"},

    # WASHINGTON
    {"name": "Archdiocese of Seattle", "address": "710 9th Avenue, Seattle, WA 98104", "website": "seattlearchdiocese.org"},
    {"name": "Diocese of Spokane", "address": "P.O. Box 1453, Spokane, WA 99210", "website": "dioceseofspokane.org"},
    {"name": "Diocese of Yakima", "address": "P.O. Box 2189, Yakima, WA 98907", "website": "yakimadiocese.org"},

    # WASHINGTON DC
    {"name": "Archdiocese for Military Services", "address": "1025 Michigan Avenue N.E., Washington, DC 20017", "website": "milarch.org"},
    {"name": "Archdiocese of Washington", "address": "P.O. Box 29260, Washington, DC 20017", "website": "adw.org"},

    # WEST VIRGINIA
    {"name": "Diocese of Wheeling-Charleston", "address": "1300 Byron Street, Wheeling, WV 26003", "website": "dwc.org"},

    # WISCONSIN
    {"name": "Archdiocese of Milwaukee", "address": "P.O. Box 70912, Milwaukee, WI 53207", "website": "archmil.org"},
    {"name": "Diocese of Green Bay", "address": "P.O. Box 23825, Green Bay, WI 54305", "website": "gbdioc.org"},
    {"name": "Diocese of La Crosse", "address": "3710 East Avenue South, La Crosse, WI 54602", "website": "diolc.org"},
    {"name": "Diocese of Madison", "address": "702 South High Point Road, Madison, WI 53719", "website": "madisondiocese.org"},
    {"name": "Diocese of Superior", "address": "1201 Hughitt Avenue, Superior, WI 54880", "website": "catholicdos.org"},

    # WYOMING
    {"name": "Diocese of Cheyenne", "address": "2121 Capitol Avenue, Cheyenne, WY 82001", "website": "dcwy.org"},
]

# Common email patterns for Catholic dioceses
EMAIL_PATTERNS = [
    "info@{domain}",
    "communications@{domain}",
    "contact@{domain}",
    "chancery@{domain}",
    "office@{domain}",
]

def derive_emails():
    """Generate probable email addresses from website domains"""
    results = []

    for diocese in DIOCESES:
        domain = diocese["website"]
        emails = []

        for pattern in EMAIL_PATTERNS:
            emails.append(pattern.format(domain=domain))

        results.append({
            "name": diocese["name"],
            "address": diocese["address"],
            "website": f"https://{domain}",
            "probable_emails": emails,
            "primary_email": f"info@{domain}"  # Most common pattern
        })

    return results

def save_results():
    """Save to JSON for use by mass emailer"""
    results = derive_emails()

    output = {
        "generated": "2025-12-26",
        "total_dioceses": len(results),
        "dioceses": results
    }

    with open("FULL_DIOCESE_EMAILS.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Generated {len(results)} diocese email records")
    print(f"Saved to FULL_DIOCESE_EMAILS.json")

    # Print first few as sample
    print("\nSample entries:")
    for d in results[:5]:
        print(f"  {d['name']}: {d['primary_email']}")

    return results

if __name__ == "__main__":
    save_results()
