import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useTranslation } from 'react-i18next';
import { z } from 'zod';
import { ArrowLeft, Save, Loader2, Hammer } from "lucide-react"

import { channelService } from '../../services/channelService';
import { ROUTES } from '../../utils/constants';
import { getErrorMessage } from '../../utils/helpers';
import type { ChannelCreate, ChannelType } from '../../types/channel';
import { CHANNEL_CONFIG_FIELDS } from '../../types/channel';

import { Button } from '../../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '../../components/ui/form';
import { Input } from '../../components/ui/input';
import { Switch } from '../../components/ui/switch';
import { Alert, AlertDescription } from '../../components/ui/alert';
import { ChannelTypeSelector } from '../../components/channels/ChannelTypeSelector';
import { ChannelConfigForm } from '../../components/channels/ChannelConfigForm';
import { TestChannelModal } from '../../components/channels/TestChannelModal';

const createFormSchema = z.object({
  name: z.string().min(1, '渠道名称不能为空').max(100, '渠道名称不能超过100个字符'),
  channel_type: z.string().min(1, '请选择渠道类型'),
  is_active: z.boolean(),
  config: z.record(z.string(), z.unknown()),
});

export function CreateChannelPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [selectedChannelType, setSelectedChannelType] = useState<string>('');
  const [showTestModal, setShowTestModal] = useState(false);
  
  const queryClient = useQueryClient();

  type FormData = z.infer<typeof createFormSchema>;

  const form = useForm<FormData>({
    resolver: zodResolver(createFormSchema),
    defaultValues: {
      name: '',
      channel_type: '',
      is_active: true,
      config: {},
    },
    mode: 'onChange',
  });

  // Watch config changes to enable/disable test button
  const config = form.watch('config');

  const createChannelMutation = useMutation({
    mutationFn: (data: ChannelCreate) => channelService.createChannel(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['channels'] });
      navigate(ROUTES.CHANNELS);
    },
  });

  const onSubmit = async (data: FormData) => {
    try {
      const channelData: ChannelCreate = {
        name: data.name,
        channel_type: data.channel_type,
        is_active: data.is_active,
        config: data.config as Record<string, unknown>,
      };
      await createChannelMutation.mutateAsync(channelData);
    } catch (error) {
      console.error('Failed to create channel:', error);
    }
  };

  const handleChannelTypeChange = (value: string) => {
    setSelectedChannelType(value);
    form.setValue('channel_type', value);
    // 清空配置
    form.setValue('config', {});
  };

  const isConfigValid = () => {
    if (!selectedChannelType) return false;
    
    const configFields = CHANNEL_CONFIG_FIELDS[selectedChannelType as ChannelType] || [];
    
    // Check if all required fields are filled
    return configFields.every(field => {
      if (!field.required) return true;
      const value = config[field.name];
      return value !== undefined && value !== null && value !== '';
    });
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center space-x-4">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => navigate(ROUTES.CHANNELS)}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          {t('common.back')}
        </Button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {t('channels.createTitle')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {t('channels.createSubtitle')}
          </p>
        </div>
      </div>

      {/* Error display */}
      {createChannelMutation.error && (
        <Alert variant="destructive">
          <AlertDescription>
            {t('errors.createChannelFailed', { message: getErrorMessage(createChannelMutation.error) })}
          </AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>{t('channels.channelConfig')}</CardTitle>
          <CardDescription>{t('channelConfig.subtitle')}</CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              {/* Basic information */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>{t('channels.channelName')} {t('channels.required')}</FormLabel>
                      <FormControl>
                        <Input
                          placeholder={t('channels.channelNamePlaceholder')}
                          disabled={createChannelMutation.isPending}
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="channel_type"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>{t('channels.channelType')} {t('channels.required')}</FormLabel>
                      <FormControl>
                        <ChannelTypeSelector
                          value={field.value}
                          onValueChange={handleChannelTypeChange}
                          disabled={createChannelMutation.isPending}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <FormField
                control={form.control}
                name="is_active"
                render={({ field }) => (
                  <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
                    <div className="space-y-0.5">
                      <FormLabel className="text-base">{t('channels.enableChannel')}</FormLabel>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {t('channels.enableChannelDesc')}
                      </div>
                    </div>
                    <FormControl>
                      <Switch
                        checked={field.value}
                        onCheckedChange={field.onChange}
                        disabled={createChannelMutation.isPending}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />

              {/* Channel-specific configuration */}
              {selectedChannelType && (
                <div className="space-y-4">
                  <div className="border-t pt-6">
                    <h3 className="text-lg font-medium mb-4">{t('channels.channelConfig')}</h3>
                    <ChannelConfigForm
                      channelType={selectedChannelType as ChannelType}
                      control={form.control}
                    />
                  </div>
                </div>
              )}

              {/* Actions */}
              <div className="flex justify-between pt-6 border-t">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowTestModal(true)}
                  disabled={
                    createChannelMutation.isPending ||
                    !selectedChannelType ||
                    !isConfigValid()
                  }
                >
                  <Hammer className="mr-2 h-4 w-4" />
                  {t('test.testChannel')}
                </Button>
                <div className="flex space-x-4">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => navigate(ROUTES.CHANNELS)}
                    disabled={createChannelMutation.isPending}
                  >
                    {t('common.cancel')}
                  </Button>
                  <Button
                    type="submit"
                    disabled={
                      createChannelMutation.isPending || !selectedChannelType
                    }
                  >
                    {createChannelMutation.isPending ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        {t('channels.creating')}
                      </>
                    ) : (
                      <>
                        <Save className="mr-2 h-4 w-4" />
                        {t('channels.createButton')}
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>

      {/* Test channel modal */}
      {selectedChannelType && (
        <TestChannelModal
          channelName={form.getValues("name") || t('test.newChannel')}
          channelType={selectedChannelType}
          open={showTestModal}
          onOpenChange={setShowTestModal}
          config={form.getValues("config")}
        />
      )}
    </div>
  )
}