import type { Channel } from './channel';

export interface Group {
  id: number;
  name: string;
  description?: string;
  token: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface GroupWithChannels extends Group {
  channels: Channel[];
}

export interface GroupCreate {
  name: string;
  description?: string;
}

export interface GroupUpdate {
  name?: string;
  description?: string;
}

export interface ChannelTestResult {
  channel_id: number;
  channel_name: string;
  success: boolean;
  message: string;
}

export interface TestGroupResponse {
  success: boolean;
  message: string;
  channel_results: ChannelTestResult[];
}