export type SportType = string;

export interface HikeListItem {
  id: string;
  title: string;
  sport: SportType;
  distance_km: number;
  duration_min: number;
  region: string;
  start_lat: number;
  start_lon: number;
}

export interface Station {
  name: string;
  operator: string | null;
  is_private_railway: boolean;
}

export interface HikeDetail extends HikeListItem {
  description: string | null;
  ascent_m: number | null;
  end_lat: number | null;
  end_lon: number | null;
  is_loop: boolean;
  geometry: Record<string, unknown> | null;
  start_station: Station | null;
  end_station: Station | null;
  source_url: string | null;
  attribution: string | null;
}