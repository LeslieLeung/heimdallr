import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Plus, Search, Filter } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

import { channelService } from '../../services/channelService';
import { ROUTES } from '../../utils/constants';
import { getErrorMessage } from '../../utils/helpers';
import type { Channel } from '../../types/channel';
import { CHANNEL_TYPES } from '../../types/channel';

import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Badge } from '../../components/ui/badge';
import { Alert, AlertDescription } from '../../components/ui/alert';
import { ChannelCard } from '../../components/channels/ChannelCard';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../components/ui/select';

export function ChannelListPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  
  const queryClient = useQueryClient();

  const { 
    data: channels = [], 
    isLoading, 
    error 
  } = useQuery({
    queryKey: ['channels'],
    queryFn: () => channelService.getChannels(),
  });

  const deleteChannelMutation = useMutation({
    mutationFn: (channelId: number) => channelService.deleteChannel(channelId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['channels'] });
    },
  });

  const updateChannelMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Channel> }) => 
      channelService.updateChannel(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['channels'] });
    },
  });

  // 过滤渠道
  const filteredChannels = Array.isArray(channels) ? channels.filter((channel) => {
    const matchesSearch = channel.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      channel.channel_type.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || 
      (statusFilter === 'active' && channel.is_active) ||
      (statusFilter === 'inactive' && !channel.is_active);
    
    const matchesType = typeFilter === 'all' || channel.channel_type === typeFilter;
    
    return matchesSearch && matchesStatus && matchesType;
  }) : [];

  // 获取所有已使用的渠道类型用于过滤
  const usedChannelTypes = Array.from(new Set(Array.isArray(channels) ? channels.map(c => c.channel_type) : []));
  // 只显示已使用的渠道类型，按照预定义顺序排序
  const availableChannelTypes = Object.values(CHANNEL_TYPES)
    .filter(type => usedChannelTypes.includes(type))
    .sort();

  const handleEdit = (channel: Channel) => {
    // 导航到编辑页面
    navigate(`/channels/${channel.id}/edit`);
  };

  const handleDelete = async (channelId: number) => {
    try {
      await deleteChannelMutation.mutateAsync(channelId);
    } catch (error) {
      console.error('Failed to delete channel:', error);
    }
  };

  const handleToggleStatus = async (channelId: number, isActive: boolean) => {
    try {
      await updateChannelMutation.mutateAsync({
        id: channelId,
        data: { is_active: isActive }
      });
    } catch (error) {
      console.error('Failed to update channel status:', error);
    }
  };

  if (error) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {t('channels.title')}
          </h1>
        </div>
        <Alert variant="destructive">
          <AlertDescription>
            {t('errors.loadChannelsFailed', { message: getErrorMessage(error) })}
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {t('channels.title')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {t('channels.subtitle')}
          </p>
        </div>
        <Button asChild>
          <Link to={ROUTES.CHANNEL_CREATE}>
            <Plus className="mr-2 h-4 w-4" />
            {t('channels.createButton')}
          </Link>
        </Button>
      </div>

      {/* Filters and search */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <Input
            placeholder={t('channels.searchPlaceholder')}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select value={statusFilter} onValueChange={(value: 'all' | 'active' | 'inactive') => setStatusFilter(value)}>
          <SelectTrigger className="w-32">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">{t('channels.allStatus')}</SelectItem>
            <SelectItem value="active">{t('common.active')}</SelectItem>
            <SelectItem value="inactive">{t('common.inactive')}</SelectItem>
          </SelectContent>
        </Select>
        <Select value={typeFilter} onValueChange={setTypeFilter}>
          <SelectTrigger className="w-40">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">{t('channels.allTypes')}</SelectItem>
            {availableChannelTypes.map((type) => (
              <SelectItem key={type} value={type}>
                {t(`channelTypes.${type}`)}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Stats */}
      <div className="flex gap-4">
        <Badge variant="outline">
          {t('channels.total', { count: Array.isArray(channels) ? channels.length : 0 })}
        </Badge>
        <Badge variant="default">
          {t('channels.activeCount', { count: Array.isArray(channels) ? channels.filter(c => c.is_active).length : 0 })}
        </Badge>
        <Badge variant="secondary">
          {t('channels.inactiveCount', { count: Array.isArray(channels) ? channels.filter(c => !c.is_active).length : 0 })}
        </Badge>
      </div>

      {/* Channels list */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-48 bg-gray-100 dark:bg-gray-800 rounded-lg animate-pulse" />
          ))}
        </div>
      ) : filteredChannels.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto h-24 w-24 text-gray-300 dark:text-gray-600">
            <Filter className="h-full w-full" />
          </div>
          <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">
            {searchTerm || statusFilter !== 'all' || typeFilter !== 'all' 
              ? t('channels.noChannelsFound')
              : t('channels.noChannelsYet')
            }
          </h3>
          <p className="mt-2 text-gray-500 dark:text-gray-400">
            {searchTerm || statusFilter !== 'all' || typeFilter !== 'all'
              ? t('channels.adjustFilters')
              : t('channels.createFirst')
            }
          </p>
          {!searchTerm && statusFilter === 'all' && typeFilter === 'all' && (
            <div className="mt-6">
              <Button asChild>
                <Link to={ROUTES.CHANNEL_CREATE}>
                  <Plus className="mr-2 h-4 w-4" />
                  {t('channels.createButton')}
                </Link>
              </Button>
            </div>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredChannels.map((channel) => (
            <ChannelCard
              key={channel.id}
              channel={channel}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onToggleStatus={handleToggleStatus}
              isLoading={deleteChannelMutation.isPending || updateChannelMutation.isPending}
            />
          ))}
        </div>
      )}
    </div>
  );
}