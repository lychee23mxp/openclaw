// Atlas Radio Club — show roster.
// Edit the soundcloudUrl for each entry to point at the real track/show URL
// (any track from soundcloud.com/atlasradioclub will embed automatically).
// Each entry needs lat/lng so it can drop a pin on the world map.
const SHOWS = [
  {
    title: "Tokyo Drift Sessions",
    host: "soraya",
    city: "Tokyo",
    country: "Japan",
    lat: 35.6762,
    lng: 139.6503,
    description: "Late-night ambient and city pop selections drifting through Shibuya backstreets.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Han River Bounce",
    host: "minjun",
    city: "Seoul",
    country: "South Korea",
    lat: 37.5665,
    lng: 126.9780,
    description: "K-house, breaks, and bedroom pop from Hongdae basements.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Monsoon Frequencies",
    host: "ananya",
    city: "Mumbai",
    country: "India",
    lat: 19.0760,
    lng: 72.8777,
    description: "Bollywood edits, qawwali fragments, and Mumbai bass — recorded mid-monsoon.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Bosphorus Static",
    host: "deniz",
    city: "Istanbul",
    country: "Turkey",
    lat: 41.0082,
    lng: 28.9784,
    description: "Anatolian psych, dub techno, and ferry-boat field recordings.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Kreuzberg Heat",
    host: "jonas",
    city: "Berlin",
    country: "Germany",
    lat: 52.5200,
    lng: 13.4050,
    description: "Slow-burn techno and dub from a basement on Skalitzer Straße.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Hackney Soup",
    host: "rae",
    city: "London",
    country: "United Kingdom",
    lat: 51.5074,
    lng: -0.1278,
    description: "Broken beat, UKG, and lover's rock simmered low and slow.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Belleville Gold",
    host: "elise",
    city: "Paris",
    country: "France",
    lat: 48.8566,
    lng: 2.3522,
    description: "Chanson, French house edits, and Maghrebi rai cassette rips.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Eko Bridge",
    host: "tunde",
    city: "Lagos",
    country: "Nigeria",
    lat: 6.5244,
    lng: 3.3792,
    description: "Afrobeats, amapiano, and Lagos street percussion clipped from a moving danfo.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Bedstuy Brownstone",
    host: "marcus",
    city: "New York",
    country: "USA",
    lat: 40.7128,
    lng: -74.0060,
    description: "Boom-bap, jazz fusion, and stoop-side conversation.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Coyoacán After Hours",
    host: "lupita",
    city: "Mexico City",
    country: "Mexico",
    lat: 19.4326,
    lng: -99.1332,
    description: "Cumbia rebajada, guaracha, and CDMX after-party tape.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Ipanema Lowtide",
    host: "bea",
    city: "Rio de Janeiro",
    country: "Brazil",
    lat: -22.9068,
    lng: -43.1729,
    description: "MPB, baile funk, and bossa pulled apart at 80 bpm.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  },
  {
    title: "Newtown Smoke",
    host: "kai",
    city: "Sydney",
    country: "Australia",
    lat: -33.8688,
    lng: 151.2093,
    description: "Down-tempo, dub, and First Nations field-recording collabs.",
    soundcloudUrl: "https://soundcloud.com/atlasradioclub"
  }
];
