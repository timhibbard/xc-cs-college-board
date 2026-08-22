/* Recruiting data. All times are the single fastest athlete, one event,
   2026 outdoor season only, from TFRRS. See methodology.html for why that
   matters. b5000 is stored in seconds for charting; null means no data. */

const ATHLETE = {
  proj5000: 920,          // ~15:20, midpoint of the 15:15-15:25 projection
  proj5000Label: '15:20',
  band: [915, 925],
};

/* tier: target | verify | caution        cs: verified | unconfirmed */
const SCHOOLS = [
  // ---------------- GREENVILLE SC (200 mi) ----------------
  { name: 'UNC Asheville',        city: 'Asheville NC',        metro: 'greenville', mi: 62,  div: 'D1', conf: 'Big South',        cs: 'unconfirmed', sat: '1120–1300', accept: '~90%', b1500: '3:51.1', b5000: 877,  tier: 'target' },
  { name: 'ETSU',                 city: 'Johnson City TN',     metro: 'greenville', mi: 140, div: 'D1', conf: 'Southern',         cs: 'unconfirmed', sat: '1010–1200', accept: '~85%', b1500: '3:47.8', b5000: 869,  tier: 'target' },
  { name: 'UNC Greensboro',       city: 'Greensboro NC',       metro: 'greenville', mi: 170, div: 'D1', conf: 'Southern',         cs: 'unconfirmed', sat: '1030–1200', accept: '~88%', b1500: '3:47.9', b5000: 869,  tier: 'target' },
  { name: 'Davidson',             city: 'Davidson NC',         metro: 'greenville', mi: 115, div: 'D1', conf: 'Atlantic 10',      cs: 'verified',    sat: '1360–1500', accept: '~18%', b1500: '3:48.3', b5000: 856,  tier: 'target', note: 'Coach support is real admissions leverage here. Pre-read early.' },
  { name: 'High Point',           city: 'High Point NC',       metro: 'greenville', mi: 180, div: 'D1', conf: 'Big South',        cs: 'unconfirmed', sat: '1090–1260', accept: '~78%', b1500: '3:43.9', b5000: 846,  tier: 'target' },
  { name: 'Elon',                 city: 'Elon NC',             metro: 'greenville', mi: 200, div: 'D1', conf: 'Coastal',          cs: 'unconfirmed', sat: '1180–1340', accept: '~78%', b1500: '4:02.3', b5000: 876,  tier: 'target' },
  { name: 'Anderson (SC)',        city: 'Anderson SC',         metro: 'greenville', mi: 30,  div: 'D2', conf: 'South Atlantic',   cs: 'unconfirmed', sat: '1000–1180', accept: '~60%', b1500: '3:48.1', b5000: 859,  tier: 'target', note: 'Site shows a BA in Applied AI and a cybersecurity center. A traditional BS in CS was NOT confirmed.' },
  { name: 'Catawba',              city: 'Salisbury NC',        metro: 'greenville', mi: 130, div: 'D2', conf: 'South Atlantic',   cs: 'unconfirmed', sat: '980–1160',  accept: '~70%', b1500: '3:46.3', b5000: 878,  tier: 'target' },
  { name: 'Lenoir-Rhyne',         city: 'Hickory NC',          metro: 'greenville', mi: 90,  div: 'D2', conf: 'South Atlantic',   cs: 'unconfirmed', sat: '1010–1190', accept: '~75%', b1500: '4:19.9', b5000: 879,  tier: 'target', note: 'The 4:19 1500 is an empty table, not a slow team. Trust the 5000.' },
  { name: 'Appalachian State',    city: 'Boone NC',            metro: 'greenville', mi: 130, div: 'D1', conf: 'Sun Belt',         cs: 'unconfirmed', sat: '1150–1290', accept: '~82%', b1500: '3:44.5', b5000: 841,  tier: 'verify', note: 'Boundary case. 7th-man data would settle it.' },
  { name: 'UNC Charlotte',        city: 'Charlotte NC',        metro: 'greenville', mi: 100, div: 'D1', conf: 'American',         cs: 'verified',    sat: '1140–1290', accept: '~80%', b1500: '3:41.2', b5000: 850,  tier: 'verify', note: 'Boundary case. 7th-man data would settle it.' },
  { name: 'Western Carolina',     city: 'Cullowhee NC',        metro: 'greenville', mi: 60,  div: 'D1', conf: 'Southern',         cs: 'unconfirmed', sat: '1030–1190', accept: '~85%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Kennesaw State',       city: 'Kennesaw GA',         metro: 'greenville', mi: 125, div: 'D1', conf: 'CUSA',             cs: 'unconfirmed', sat: '1050–1220', accept: '~75%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Georgia State',        city: 'Atlanta GA',          metro: 'greenville', mi: 150, div: 'D1', conf: 'Sun Belt',         cs: 'unconfirmed', sat: '1030–1210', accept: '~70%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Lander',               city: 'Greenwood SC',        metro: 'greenville', mi: 55,  div: 'D2', conf: 'Peach Belt',       cs: 'unconfirmed', sat: '980–1150',  accept: '~55%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Carson-Newman',        city: 'Jefferson City TN',   metro: 'greenville', mi: 150, div: 'D2', conf: 'South Atlantic',   cs: 'unconfirmed', sat: '980–1170',  accept: '~75%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'King University',      city: 'Bristol TN',          metro: 'greenville', mi: 155, div: 'D2', conf: 'Conf. Carolinas',  cs: 'unconfirmed', sat: '950–1150',  accept: '~70%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Piedmont University',  city: 'Demorest GA',         metro: 'greenville', mi: 100, div: 'D3', conf: 'USA South',        cs: 'unconfirmed', sat: '1000–1190', accept: '~65%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Presbyterian',         city: 'Clinton SC',          metro: 'greenville', mi: 45,  div: 'D1', conf: 'Big South',        cs: 'unconfirmed', sat: '1030–1210', accept: '~75%', b1500: '4:02.5', b5000: 897,  tier: 'caution' },
  { name: 'USC Upstate',          city: 'Spartanburg SC',      metro: 'greenville', mi: 32,  div: 'D1', conf: 'Big South',        cs: 'unconfirmed', sat: '1000–1160', accept: '~65%', b1500: '3:53.0', b5000: 907,  tier: 'caution' },
  { name: 'Emory',                city: 'Atlanta GA',          metro: 'greenville', mi: 145, div: 'D3', conf: 'UAA',              cs: 'verified',    sat: '1450–1550', accept: '~13%', b1500: '3:49.5', b5000: 906,  tier: 'caution', note: 'Elite CS. No athletic aid at D3, but strong need-based aid. Coach pre-read matters.' },
  { name: 'Berry College',        city: 'Rome GA',             metro: 'greenville', mi: 150, div: 'D3', conf: 'SAA',              cs: 'unconfirmed', sat: '1150–1330', accept: '~65%', b1500: '3:57.5', b5000: 900,  tier: 'caution' },
  { name: 'Winthrop',             city: 'Rock Hill SC',        metro: 'greenville', mi: 100, div: 'D1', conf: 'Big South',        cs: 'unconfirmed', sat: '1010–1180', accept: '~80%', b1500: '3:59.1', b5000: 925,  tier: 'caution' },
  { name: 'Wofford',              city: 'Spartanburg SC',      metro: 'greenville', mi: 32,  div: 'D1', conf: 'Southern',         cs: 'verified',    sat: '1220–1390', accept: '~70%', b1500: '3:55.7', b5000: 927,  tier: 'caution', note: 'Sharpest version of the trade-off: strong academics, verified CS, 32 miles, and a team best he beats on arrival.' },
  { name: 'North Greenville',     city: 'Tigerville SC',       metro: 'greenville', mi: 25,  div: 'D2', conf: 'Conf. Carolinas',  cs: 'unconfirmed', sat: '980–1160',  accept: '~60%', b1500: '4:01.3', b5000: 947,  tier: 'caution' },
  { name: 'Gardner-Webb',         city: 'Boiling Springs NC',  metro: 'greenville', mi: 60,  div: 'D1', conf: 'Big South',        cs: 'unconfirmed', sat: '1000–1180', accept: '~80%', b1500: '4:13.0', b5000: 993,  tier: 'caution' },
  { name: 'Guilford',             city: 'Greensboro NC',       metro: 'greenville', mi: 180, div: 'D3', conf: 'ODAC',             cs: 'unconfirmed', sat: '1000–1200', accept: '~78%', b1500: null,     b5000: null, tier: 'caution', note: 'Almost no distance data at all. Only mark found was a 10:46 3000.' },

  // ---------------- NEW YORK CITY (50 mi) ----------------
  { name: 'Fordham',              city: 'Bronx NY',            metro: 'nyc', mi: 8,  div: 'D1', conf: 'Atlantic 10',     cs: 'verified',    sat: '1320–1470', accept: '~54%', b1500: '3:49.4', b5000: 891,  tier: 'target', note: 'Trains at Van Cortlandt Park, the historic US cross country course, next to campus.' },
  { name: 'Wagner',               city: 'Staten Island NY',    metro: 'nyc', mi: 12, div: 'D1', conf: 'NEC',             cs: 'unconfirmed', sat: '1050–1230', accept: '~80%', b1500: '3:47.9', b5000: 871,  tier: 'target' },
  { name: 'Hofstra',              city: 'Hempstead NY',        metro: 'nyc', mi: 25, div: 'D1', conf: 'Coastal',         cs: 'unconfirmed', sat: '1180–1340', accept: '~70%', b1500: '3:48.2', b5000: 872,  tier: 'target' },
  { name: 'Seton Hall',           city: 'South Orange NJ',     metro: 'nyc', mi: 18, div: 'D1', conf: 'Big East',        cs: 'verified',    sat: '1180–1350', accept: '~75%', b1500: '4:01.3', b5000: 898,  tier: 'target', note: 'Distance squad is weaker than the Big East name suggests, which works in his favor.' },
  { name: 'Fairfield',            city: 'Fairfield CT',        metro: 'nyc', mi: 50, div: 'D1', conf: 'MAAC',            cs: 'unconfirmed', sat: '1250–1400', accept: '~57%', b1500: '4:00.2', b5000: 899,  tier: 'target' },
  { name: 'NYU',                  city: 'Manhattan NY',        metro: 'nyc', mi: 0,  div: 'D3', conf: 'UAA',             cs: 'verified',    sat: '1470–1570', accept: '~9%',  b1500: '3:49.4', b5000: 836,  tier: 'verify', note: 'Borderline. Top-tier D3 program; he likely would not travel as a freshman.' },
  { name: 'NJIT',                 city: 'Newark NJ',           metro: 'nyc', mi: 12, div: 'D1', conf: 'America East',    cs: 'verified',    sat: '1230–1410', accept: '~65%', b1500: null,     b5000: null, tier: 'verify', note: 'Best D1-plus-CS value in the metro if the running fits. Needs roster data.' },
  { name: 'Stevens Institute',    city: 'Hoboken NJ',          metro: 'nyc', mi: 3,  div: 'D3', conf: 'MAC',             cs: 'verified',    sat: '1400–1520', accept: '~45%', b1500: null,     b5000: null, tier: 'verify', note: 'Strongest CS on the D3 list. Get roster times before investing.' },
  { name: 'Fairleigh Dickinson',  city: 'Teaneck NJ',          metro: 'nyc', mi: 12, div: 'D1', conf: 'NEC',             cs: 'unconfirmed', sat: '1000–1190', accept: '~90%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Monmouth',            city: 'W. Long Branch NJ',   metro: 'nyc', mi: 45, div: 'D1', conf: 'Coastal',         cs: 'unconfirmed', sat: '1080–1250', accept: '~85%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Army West Point',      city: 'West Point NY',       metro: 'nyc', mi: 50, div: 'D1', conf: 'Patriot',         cs: 'verified',    sat: '1200–1400', accept: '~11%', b1500: null,     b5000: null, tier: 'verify', note: 'Requires a congressional nomination and a 5-year active-duty service obligation. A different life decision, not just a college choice.' },
  { name: 'Adelphi',              city: 'Garden City NY',      metro: 'nyc', mi: 25, div: 'D2', conf: 'NE10',            cs: 'unconfirmed', sat: '1080–1260', accept: '~75%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Molloy',               city: 'Rockville Centre NY', metro: 'nyc', mi: 25, div: 'D2', conf: 'ECC',             cs: 'unconfirmed', sat: '1000–1190', accept: '~80%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Pace',                 city: 'Pleasantville NY',    metro: 'nyc', mi: 30, div: 'D2', conf: 'NE10',            cs: 'unconfirmed', sat: '1080–1260', accept: '~85%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Mercy University',     city: 'Dobbs Ferry NY',      metro: 'nyc', mi: 25, div: 'D2', conf: 'ECC',             cs: 'unconfirmed', sat: '940–1120',  accept: '~90%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Queens College (CUNY)',city: 'Queens NY',           metro: 'nyc', mi: 10, div: 'D2', conf: 'ECC',             cs: 'unconfirmed', sat: '1010–1200', accept: '~55%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'NYIT',                 city: 'Old Westbury NY',     metro: 'nyc', mi: 25, div: 'D2', conf: 'ECC',             cs: 'verified',    sat: '1080–1280', accept: '~75%', b1500: null,     b5000: null, tier: 'verify', note: 'Confirm they still sponsor men’s cross country.' },
  { name: 'St. Thomas Aquinas',   city: 'Sparkill NY',         metro: 'nyc', mi: 20, div: 'D2', conf: 'CACC',            cs: 'unconfirmed', sat: '950–1140',  accept: '~90%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Montclair State',      city: 'Montclair NJ',        metro: 'nyc', mi: 15, div: 'D3', conf: 'NJAC',            cs: 'unconfirmed', sat: '1030–1210', accept: '~90%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Kean University',      city: 'Union NJ',            metro: 'nyc', mi: 20, div: 'D3', conf: 'NJAC',            cs: 'unconfirmed', sat: '970–1150',  accept: '~90%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Ramapo College',       city: 'Mahwah NJ',           metro: 'nyc', mi: 25, div: 'D3', conf: 'NJAC',            cs: 'unconfirmed', sat: '1080–1250', accept: '~80%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'William Paterson',     city: 'Wayne NJ',            metro: 'nyc', mi: 20, div: 'D3', conf: 'NJAC',            cs: 'unconfirmed', sat: '950–1140',  accept: '~95%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Baruch College',       city: 'Manhattan NY',        metro: 'nyc', mi: 5,  div: 'D3', conf: 'CUNYAC',          cs: 'unconfirmed', sat: '1240–1420', accept: '~50%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Yeshiva University',   city: 'Manhattan NY',        metro: 'nyc', mi: 5,  div: 'D3', conf: 'Skyline',         cs: 'unconfirmed', sat: '1200–1400', accept: '~60%', b1500: null,     b5000: null, tier: 'verify' },
  { name: "St. Joseph's Univ NY", city: 'Brooklyn NY',         metro: 'nyc', mi: 10, div: 'D3', conf: 'Skyline',         cs: 'unconfirmed', sat: '1030–1210', accept: '~80%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Drew University',      city: 'Madison NJ',          metro: 'nyc', mi: 30, div: 'D3', conf: 'Landmark',        cs: 'unconfirmed', sat: '1080–1290', accept: '~70%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Farmingdale State',    city: 'Farmingdale NY',      metro: 'nyc', mi: 35, div: 'D3', conf: 'Skyline',         cs: 'verified',    sat: '1000–1180', accept: '~65%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Manhattanville',       city: 'Purchase NY',         metro: 'nyc', mi: 30, div: 'D3', conf: 'Skyline',         cs: 'unconfirmed', sat: '970–1170',  accept: '~90%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'SUNY Purchase',        city: 'Purchase NY',         metro: 'nyc', mi: 30, div: 'D3', conf: 'Skyline',         cs: 'unconfirmed', sat: '1030–1230', accept: '~75%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Mount Saint Vincent',  city: 'Bronx NY',            metro: 'nyc', mi: 12, div: 'D3', conf: 'Skyline',         cs: 'unconfirmed', sat: '970–1160',  accept: '~85%', b1500: null,     b5000: null, tier: 'verify' },
  { name: 'Merchant Marine Acad.',city: 'Kings Point NY',      metro: 'nyc', mi: 20, div: 'D3', conf: 'Skyline',         cs: 'unconfirmed', sat: '1180–1380', accept: '~25%', b1500: null,     b5000: null, tier: 'verify', note: 'Carries a service obligation.' },
  { name: 'Manhattan',            city: 'Bronx NY',            metro: 'nyc', mi: 10, div: 'D1', conf: 'MAAC',            cs: 'unconfirmed', sat: '1080–1260', accept: '~85%', b1500: '4:01.4', b5000: 903,  tier: 'caution' },
  { name: 'LIU',                  city: 'Brooklyn NY',         metro: 'nyc', mi: 5,  div: 'D1', conf: 'NEC',             cs: 'unconfirmed', sat: '1010–1200', accept: '~80%', b1500: '3:44.9', b5000: 912,  tier: 'caution' },
  { name: 'Sacred Heart',         city: 'Fairfield CT',        metro: 'nyc', mi: 50, div: 'D1', conf: 'NEC',             cs: 'unconfirmed', sat: '1090–1260', accept: '~75%', b1500: '3:57.9', b5000: 922,  tier: 'caution' },
  { name: "Saint Peter's",        city: 'Jersey City NJ',      metro: 'nyc', mi: 5,  div: 'D1', conf: 'MAAC',            cs: 'unconfirmed', sat: '950–1140',  accept: '~85%', b1500: '4:07.8', b5000: 950,  tier: 'caution' },

  // ---------------- CHICAGO (20 mi) ----------------
  { name: 'DePaul',               city: 'Lincoln Park',        metro: 'chicago', mi: 3,  div: 'D1',   conf: 'Big East',       cs: 'verified', sat: '1090–1290', accept: '~70%', b1500: '3:43.8', b5000: 862,  tier: 'target', note: 'Best fit inside the radius. 8:23 3000 and 29:52 10K confirm a functioning distance squad.' },
  { name: 'Loyola Chicago',       city: 'Rogers Park',         metro: 'chicago', mi: 8,  div: 'D1',   conf: 'Atlantic 10',    cs: 'verified', sat: '1150–1330', accept: '~80%', b1500: '3:40.5', b5000: 863,  tier: 'target' },
  { name: 'UIC',                  city: 'Near West Side',      metro: 'chicago', mi: 3,  div: 'D1',   conf: 'Missouri Valley',cs: 'verified', sat: '1050–1260', accept: '~80%', b1500: '3:48.5', b5000: 836,  tier: 'verify', note: 'Boundary. Strong top end (28:56 10K) but no depth data. Resolve this first.' },
  { name: 'University of Chicago',city: 'Hyde Park',           metro: 'chicago', mi: 7,  div: 'D3',   conf: 'UAA',            cs: 'verified', sat: '1510–1580', accept: '~5%',  b1500: null,     b5000: null, tier: 'verify', note: 'Could not resolve their TFRRS page. Potentially the best combined fit in the metro and currently a blank.' },
  { name: 'Chicago State',        city: 'Far South Side',      metro: 'chicago', mi: 10, div: 'D1',   conf: 'NEC',            cs: 'unconfirmed', sat: '850–1030', accept: '~60%', b1500: null,   b5000: null, tier: 'verify' },
  { name: 'Saint Xavier',         city: 'Southwest Side',      metro: 'chicago', mi: 13, div: 'NAIA', conf: 'CCAC',           cs: 'unconfirmed', sat: '990–1180', accept: '~80%', b1500: null,   b5000: null, tier: 'verify' },
  { name: 'Trinity Christian',    city: 'Palos Heights',       metro: 'chicago', mi: 20, div: 'NAIA', conf: 'CCAC',           cs: 'unconfirmed', sat: '970–1170', accept: '~85%', b1500: null,   b5000: null, tier: 'verify' },
  { name: 'Calumet College',      city: 'Whiting IN',          metro: 'chicago', mi: 20, div: 'NAIA', conf: 'CCAC',           cs: 'unconfirmed', sat: '900–1100', accept: '~90%', b1500: null,   b5000: null, tier: 'verify' },
  { name: 'Elmhurst University',  city: 'Elmhurst',            metro: 'chicago', mi: 16, div: 'D3',   conf: 'CCIW',           cs: 'unconfirmed', sat: '1010–1220', accept: '~75%', b1500: '4:09.5', b5000: 916, tier: 'caution' },
  { name: 'Concordia Chicago',    city: 'River Forest',        metro: 'chicago', mi: 10, div: 'D3',   conf: 'CCIW',           cs: 'unconfirmed', sat: '970–1170',  accept: '~90%', b1500: '4:12.0', b5000: 991, tier: 'caution' },
  { name: 'Dominican University', city: 'River Forest',        metro: 'chicago', mi: 10, div: 'D3',   conf: 'NACC',           cs: 'unconfirmed', sat: '950–1140',  accept: '~85%', b1500: '4:12.2', b5000: null, tier: 'caution', note: 'Only distance mark on record is a 1500. Thin corps.' },
  { name: 'North Park University',city: 'North Park',          metro: 'chicago', mi: 8,  div: 'D3',   conf: 'CCIW',           cs: 'unconfirmed', sat: '990–1190',  accept: '~85%', b1500: '4:27.6', b5000: 1022, tier: 'caution' },
  { name: 'Illinois Tech',        city: 'Bronzeville',         metro: 'chicago', mi: 4,  div: 'D3',   conf: 'NACC',           cs: 'verified',    sat: '1290–1450', accept: '~60%', b1500: '4:25.1', b5000: 1066, tier: 'caution', note: 'Top CS program 4 miles from downtown, but he would beat their best runner by two and a half minutes. Not a training environment.' },
];

/* Cut because his projected marks put him well off the back of the roster:
   no realistic scholarship or scoring role as a freshman. */
const REMOVED = [
  { name: 'Furman',            metro: 'greenville', div: 'D1 Southern',       why: 'Team best 5000 <b>13:40</b>. Nationally elite; ~1:40 gap. Also 0 miles away with a verified CS degree, which is what makes the cut hurt.' },
  { name: 'Clemson',           metro: 'greenville', div: 'D1 ACC',            why: 'ACC program 32 miles away. Their 1500 best of 3:43 implies a ~14:15 5K runner even though the outdoor 5000 table reads 14:36.' },
  { name: 'Georgia Tech',      metro: 'greenville', div: 'D1 ACC',            why: '5000 <b>13:41</b>, 10K 29:45. Also the hardest CS admit on the list — GT CS is far more selective than the overall rate suggests.' },
  { name: 'Wingate',           metro: 'greenville', div: 'D2 South Atlantic', why: '5000 <b>13:37</b>, 10K 29:20. The strongest D2 distance program in the region.' },
  { name: 'Tennessee',         metro: 'greenville', div: 'D1 SEC',            why: 'Out of range.' },
  { name: 'Georgia',           metro: 'greenville', div: 'D1 SEC',            why: 'Out of range.' },
  { name: 'Wake Forest',       metro: 'greenville', div: 'D1 ACC',            why: 'Out of range.' },
  { name: 'South Carolina',    metro: 'greenville', div: 'D1 SEC',            why: 'Out of range.' },
  { name: 'Columbia',          metro: 'nyc',        div: 'D1 Ivy',            why: '5000 <b>13:43</b>, 3000 8:30, 10K 29:09. Elite — and one of the best CS departments in the country, which is what makes this cut expensive.' },
  { name: 'Iona',              metro: 'nyc',        div: 'D1 MAAC',           why: '5000 <b>14:03</b>, 10K 29:02, 1500 3:38. A national cross country program, 20 miles out.' },
  { name: 'Princeton',         metro: 'nyc',        div: 'D1 Ivy',            why: 'Elite Ivy distance squad at ~50 miles.' },
  { name: "St. John's",        metro: 'nyc',        div: 'D1 Big East',       why: 'Nationally strong Big East distance program.' },
  { name: 'Rutgers',           metro: 'nyc',        div: 'D1 Big Ten',        why: 'Big Ten; out of range.' },
  { name: 'North Central',     metro: 'chicago',    div: 'D3 CCIW',           why: 'Perennial national champion, 28 miles out. Excluded on merit, not distance.' },
  { name: 'Wheaton College',   metro: 'chicago',    div: 'D3 CCIW',           why: 'National-caliber D3 program, 25 miles out.' },
];

/* Northwestern is not a removal — there is no men's program to be removed from. */
const NO_PROGRAM = [
  { name: 'Northwestern', metro: 'chicago', why: 'Does not sponsor men’s cross country <em>or</em> men’s track and field. Men’s track is listed as defunct; only the women’s programs exist. Verified — worth stating plainly because Northwestern is the obvious first thought for Chicago plus elite CS, and it simply is not available to him.' },
];

const OUTSIDE_RADIUS = [
  { name: 'Lewis University',  mi: 30, div: 'D2 GLVC',       why: 'Probably the single best fit in metro Chicago. Strong distance program, CS degree, and D2 scholarship money.' },
  { name: 'Benedictine',       mi: 25, div: 'D3 NACC',       why: 'Plausible fit.' },
  { name: 'Purdue Northwest',  mi: 25, div: 'D2 GLIAC',      why: 'Hammond IN. Plausible fit.' },
  { name: 'Lake Forest',       mi: 30, div: 'D3 Midwest',    why: 'Plausible fit.' },
];

const METROS = {
  greenville: { label: 'Greenville SC', radius: '200 mi', page: 'greenville.html' },
  nyc:        { label: 'New York City', radius: '50 mi',  page: 'new-york.html' },
  chicago:    { label: 'Chicago',       radius: '20 mi',  page: 'chicago.html' },
};

const TIERS = {
  target:  { label: 'Target',  glyph: '▲', desc: 'Ideal development band — he would slot in around 5th to 9th man' },
  verify:  { label: 'Verify',  glyph: '◆', desc: 'Boundary case or no roster data yet — get the numbers before investing' },
  caution: { label: 'Caution', glyph: '▼', desc: 'He would arrive at or near #1 — thin training group' },
};
