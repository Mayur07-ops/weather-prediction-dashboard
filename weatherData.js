/**
 * weatherData.js
 * ─────────────────────────────────────────────────────────────
 * All static data derived from weather.csv (366 days, 22 features).
 * Imported by charts.js and model.js.
 */

const MONTHS = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12'];

/** Monthly average max temperatures (°C) */
const AVG_MAX_TEMP = [25.1, 24.8, 29.1, 25.2, 26.2, 19.8, 17.0, 14.8, 12.0, 12.3, 17.1, 21.9];

/** Monthly average min temperatures (°C) */
const AVG_MIN_TEMP = [11.8, 13.3, 15.1, 13.2, 11.0, 5.8, 2.5, 4.4, 0.1, 0.0, 2.9, 6.4];

/** Monthly total rainfall (mm) */
const MONTHLY_RAINFALL = [95.4, 101.0, 38.6, 59.4, 40.4, 17.2, 12.8, 22.0, 42.6, 15.0, 44.8, 33.6];

/** Monthly average afternoon humidity (%) */
const MONTHLY_HUMIDITY = [42.2, 50.3, 38.8, 46.0, 35.8, 41.5, 46.8, 59.2, 57.9, 48.8, 38.7, 32.0];

/** Max temperature distribution (days per band: ≤10, 11-15, 16-20, 21-25, 26-30, >30) */
const TEMP_DIST = [9, 83, 98, 78, 62, 36];
const TEMP_DIST_LABELS = ['≤10°', '11–15°', '16–20°', '21–25°', '26–30°', '>30°'];

/** Afternoon humidity distribution (days per band: 0-20, 21-40, 41-60, 61-80, 81-100) */
const HUMIDITY_DIST = [20, 143, 140, 51, 12];
const HUMIDITY_DIST_LABELS = ['0–20%', '21–40%', '41–60%', '61–80%', '81–100%'];

/** Morning cloud cover distribution (days: clear 0-2, partly 3-5, overcast 6-8) */
const CLOUD_DIST = [166, 49, 151];
const CLOUD_DIST_LABELS = ['Clear\n(0–2)', 'Partly\n(3–5)', 'Overcast\n(6–8)'];

/** Top 8 wind gust directions (ascending by count) */
const WIND_DIRS   = ['N', 'S', 'ESE', 'ENE', 'WNW', 'E', 'NNW', 'NW'];
const WIND_COUNTS = [21, 22, 23, 30, 35, 37, 44, 73];

/** Rain Today / Rain Tomorrow yes/no counts */
const RAIN_DATA = [
  { value: 66,  name: 'Rain Today: Yes' },
  { value: 300, name: 'Rain Today: No'  },
  { value: 66,  name: 'Rain Tomorrow: Yes' },
  { value: 300, name: 'Rain Tomorrow: No'  },
];

/** Summary KPI values */
const KPI = {
  avgMaxTemp:  20.6,
  avgMinTemp:  7.3,
  peakTemp:    35.8,
  lowestTemp: -5.3,
  avgHumidity: 44.5,
  rainDays:    66,
  totalDays:   366,
  avgRainfall: 1.43,
  avgWindGust: 39.7,
};

/** Model evaluation results */
const MODEL = {
  accuracy:       74.9,
  samples:        366,
  truePositives:  49,
  trueNegatives:  225,
  falsePositives: 75,
  falseNegatives: 17,
  rule: 'IF Humidity3pm > 60% OR Rainfall > 1mm → RainTomorrow = Yes',
  featureImportance: [
    { name: 'Humidity 3pm',   pct: 88 },
    { name: 'Rainfall Today', pct: 75 },
    { name: 'Cloud Cover 9am',pct: 55 },
    { name: 'Wind Gust Speed',pct: 38 },
    { name: 'Pressure 9am',   pct: 28 },
  ],
  seasonalRisk: [
    { name: 'Summer (M1–M3)',  label: 'High',   days: 23, pct: 77 },
    { name: 'Autumn (M4–M6)',  label: 'Medium', days: 17, pct: 57 },
    { name: 'Winter (M7–M9)',  label: 'Low',    days: 12, pct: 40 },
    { name: 'Spring (M10–M12)',label: 'Low',    days: 14, pct: 47 },
  ],
};
