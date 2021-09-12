from csep.utils import time_utils

config = {
    'start_date': time_utils.strptime_to_utc_datetime('2006-01-01 00:00:00.0'),
    'end_date': time_utils.strptime_to_utc_datetime('2011-01-01 00:00:00.0'),
    'forecasts': {
        'shen': './forecasts/shen_et_al.geodetic.aftershock-fromXML.dat',
        'kagan': './forecasts/kagan_et_al.aftershock-fromXML.dat',
        'helmstetter': './forecasts/helmstetter_et_al.hkj.aftershock-fromXML.dat',
        'ebel': './forecasts/ebel.aftershock.corrected-fromXML.dat',
        'ebel_uncorrected': './forecasts/ebel.aftershock-fromXML.dat',
        'bird_liu': './forecasts/bird_liu.neokinema-fromXML.dat'
    },
    'seed': 12345,
    'nsims': 1000000
}


