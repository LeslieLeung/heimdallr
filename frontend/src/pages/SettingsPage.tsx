import { useState } from 'react';
import { useQuery } from "@tanstack/react-query"
import { useTranslation } from "react-i18next"
import { useVersion } from "../hooks/useVersion"
import {
  Settings,
  Palette,
  Monitor,
  Sun,
  Moon,
  Bell,
  Shield,
  Database,
  Download,
  Upload,
  Trash2,
  AlertTriangle,
  Check,
  Globe,
  RotateCcw,
  ExternalLink,
  Info,
} from "lucide-react"

import { useTheme } from "../contexts/ThemeContext"
import { useLanguage } from "../contexts/LanguageContext"
import { authService } from "../services/authService"
import { groupService } from "../services/groupService"
import { channelService } from "../services/channelService"
import { THEMES } from "../utils/constants"

import { Button } from "../components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../components/ui/card"
import { Alert, AlertDescription, AlertTitle } from "../components/ui/alert"
import { Badge } from "../components/ui/badge"
import { Separator } from "../components/ui/separator"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../components/ui/select"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "../components/ui/alert-dialog"
import UpdateModal from "../components/version/UpdateModal"

type Theme = (typeof THEMES)[keyof typeof THEMES]

export function SettingsPage() {
  const { t } = useTranslation()
  const { theme, setTheme } = useTheme()
  const { language, setLanguage, availableLanguages } = useLanguage()
  const { currentVersion, isCheckingUpdate, updateInfo, forceCheckUpdates } = useVersion()
  const [exportSuccess, setExportSuccess] = useState(false)
  const [showUpdateModal, setShowUpdateModal] = useState(false)

  // Fetch user data
  const { data: user } = useQuery({
    queryKey: ["user", "profile"],
    queryFn: () => authService.getCurrentUser(),
  })

  // Fetch statistics
  const { data: groups = [] } = useQuery({
    queryKey: ["groups"],
    queryFn: () => groupService.getGroups(),
  })

  const { data: channels = [] } = useQuery({
    queryKey: ["channels"],
    queryFn: () => channelService.getChannels(),
  })

  const handleThemeChange = (newTheme: Theme) => {
    setTheme(newTheme)
  }

  const handleCheckUpdates = async () => {
    try {
      await forceCheckUpdates()
      if (updateInfo?.hasUpdate) {
        setShowUpdateModal(true)
      }
    } catch (error) {
      console.error('Failed to check for updates:', error)
    }
  }

  const handleExportData = async () => {
    try {
      // 获取所有数据
      const [groupsData, channelsData] = await Promise.all([
        groupService.getGroups(),
        channelService.getChannels(),
      ])

      // 构造导出数据
      const exportData = {
        version: currentVersion || "3.0.0",
        timestamp: new Date().toISOString(),
        data: {
          groups: groupsData.map((group) => ({
            name: group.name,
            description: group.description,
          })),
          channels: channelsData.map((channel) => ({
            name: channel.name,
            channel_type: channel.channel_type,
            config: channel.config,
            is_active: channel.is_active,
          })),
        },
      }

      // 下载文件
      const blob = new Blob([JSON.stringify(exportData, null, 2)], {
        type: "application/json",
      })
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `heimdallr-export-${
        new Date().toISOString().split("T")[0]
      }.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)

      setExportSuccess(true)
      setTimeout(() => setExportSuccess(false), 3000)
    } catch (error) {
      console.error("Failed to export data:", error)
    }
  }

  const getThemeIcon = (selectedTheme: Theme) => {
    switch (selectedTheme) {
      case THEMES.LIGHT:
        return <Sun className="h-4 w-4" />
      case THEMES.DARK:
        return <Moon className="h-4 w-4" />
      default:
        return <Monitor className="h-4 w-4" />
    }
  }

  const getThemeLabel = (selectedTheme: Theme) => {
    switch (selectedTheme) {
      case THEMES.LIGHT:
        return t("settings.appearance.lightTheme")
      case THEMES.DARK:
        return t("settings.appearance.darkTheme")
      default:
        return t("settings.appearance.systemTheme")
    }
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          {t("settings.title")}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          {t("settings.subtitle")}
        </p>
      </div>

      {/* Export success message */}
      {exportSuccess && (
        <Alert>
          <Check className="h-4 w-4" />
          <AlertTitle>{t("settings.exportSuccess")}</AlertTitle>
          <AlertDescription>{t("settings.exportSuccessDesc")}</AlertDescription>
        </Alert>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Appearance Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Palette className="h-5 w-5" />
              <span>{t("settings.appearance.title")}</span>
            </CardTitle>
            <CardDescription>
              {t("settings.appearance.subtitle")}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Theme selection */}
            <div className="space-y-3">
              <label className="text-sm font-medium">
                {t("settings.appearance.themeMode")}
              </label>
              <Select value={theme} onValueChange={handleThemeChange}>
                <SelectTrigger>
                  <SelectValue>
                    <div className="flex items-center space-x-2">
                      {getThemeIcon(theme)}
                      <span>{getThemeLabel(theme)}</span>
                    </div>
                  </SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={THEMES.LIGHT}>
                    <div className="flex items-center space-x-2">
                      <Sun className="h-4 w-4" />
                      <span>{t("settings.appearance.lightTheme")}</span>
                    </div>
                  </SelectItem>
                  <SelectItem value={THEMES.DARK}>
                    <div className="flex items-center space-x-2">
                      <Moon className="h-4 w-4" />
                      <span>{t("settings.appearance.darkTheme")}</span>
                    </div>
                  </SelectItem>
                  <SelectItem value={THEMES.SYSTEM}>
                    <div className="flex items-center space-x-2">
                      <Monitor className="h-4 w-4" />
                      <span>{t("settings.appearance.systemTheme")}</span>
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Separator />

            {/* Language selection */}
            <div className="space-y-3">
              <label className="text-sm font-medium">
                {t("settings.appearance.language")}
              </label>
              <Select value={language} onValueChange={setLanguage}>
                <SelectTrigger>
                  <SelectValue>
                    <div className="flex items-center space-x-2">
                      <Globe className="h-4 w-4" />
                      <span>
                        {availableLanguages.find(
                          (lang) => lang.value === language
                        )?.label || t("language.zh")}
                      </span>
                    </div>
                  </SelectValue>
                </SelectTrigger>
                <SelectContent>
                  {availableLanguages.map((lang) => (
                    <SelectItem key={lang.value} value={lang.value}>
                      <div className="flex items-center space-x-2">
                        <Globe className="h-4 w-4" />
                        <span>{lang.label}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {t("settings.appearance.languageDesc")}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Notification Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Bell className="h-5 w-5" />
              <span>{t("settings.notifications.title")}</span>
            </CardTitle>
            <CardDescription>
              {t("settings.notifications.subtitle")}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <p className="text-gray-500 dark:text-gray-400 text-center py-8">{t("settings.notifications.underConstruction")}</p>
            </div>
          </CardContent>
        </Card>

        {/* System Info */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Database className="h-5 w-5" />
              <span>{t("settings.systemInfo.title")}</span>
            </CardTitle>
            <CardDescription>
              {t("settings.systemInfo.subtitle")}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* User info */}
            {user && (
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <p className="text-sm font-medium">
                    {t("settings.systemInfo.currentUser")}
                  </p>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {user.username}
                    </span>
                    {user.is_admin && (
                      <Badge variant="default" className="h-5 text-xs">
                        <Shield className="h-3 w-3 mr-1" />
                        {t("settings.systemInfo.administrator")}
                      </Badge>
                    )}
                  </div>
                </div>
              </div>
            )}

            <Separator />

            {/* Statistics */}
            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {channels.length}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {t("settings.systemInfo.notificationChannels")}
                </p>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {groups.length}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {t("settings.systemInfo.notificationGroups")}
                </p>
              </div>
            </div>

            <Separator />

            {/* Active channels */}
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <p className="text-sm font-medium">
                  {t("settings.systemInfo.activeChannels")}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {t("settings.systemInfo.activeChannelsDesc")}
                </p>
              </div>
              <Badge variant="outline">
                {channels.filter((c) => c.is_active).length} / {channels.length}
              </Badge>
            </div>
          </CardContent>
        </Card>

        {/* Data Management */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Settings className="h-5 w-5" />
              <span>{t("settings.dataManagement.title")}</span>
            </CardTitle>
            <CardDescription>
              {t("settings.dataManagement.subtitle")}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Export data */}
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <p className="text-sm font-medium">
                  {t("settings.dataManagement.exportData")}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {t("settings.dataManagement.exportDataDesc")}
                </p>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={handleExportData}
                disabled={channels.length === 0 && groups.length === 0}
              >
                <Download className="h-4 w-4 mr-2" />
                {t("settings.dataManagement.exportData")}
              </Button>
            </div>

            <Separator />

            {/* Import data placeholder */}
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <p className="text-sm font-medium">
                  {t("settings.dataManagement.importData")}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {t("settings.dataManagement.importDataDesc")}
                </p>
              </div>
              <Button variant="outline" size="sm" disabled>
                <Upload className="h-4 w-4 mr-2" />
                {t("settings.dataManagement.importData")}
              </Button>
            </div>

            <Separator />

            {/* Dangerous actions */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2 text-red-600 dark:text-red-400">
                <AlertTriangle className="h-4 w-4" />
                <span className="text-sm font-medium">
                  {t("settings.dataManagement.dangerZone")}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <p className="text-sm font-medium">
                    {t("settings.dataManagement.clearAllData")}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {t("settings.dataManagement.clearAllDataDesc")}
                  </p>
                </div>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button variant="destructive" size="sm">
                      <Trash2 className="h-4 w-4 mr-2" />
                      {t("settings.dataManagement.clearAllData")}
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>
                        {t("settings.dataManagement.clearConfirmTitle")}
                      </AlertDialogTitle>
                      <AlertDialogDescription>
                        {t("settings.dataManagement.clearConfirmDesc")}
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>
                        {t("common.cancel")}
                      </AlertDialogCancel>
                      <AlertDialogAction
                        className="bg-red-600 hover:bg-red-700"
                        disabled
                      >
                        {t("settings.dataManagement.confirmClear")}
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Version & Updates section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Info className="h-5 w-5" />
            <span>{t("settings.about.title")}</span>
          </CardTitle>
          <CardDescription>{t("settings.about.subtitle")}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Current version */}
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <p className="text-sm font-medium">
                {t("settings.about.currentVersion")}
              </p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                v{currentVersion || '3.0.0'}
              </p>
            </div>
            {updateInfo?.hasUpdate && (
              <Badge variant="default" className="bg-green-600">
                {t("settings.about.updateAvailable")}
              </Badge>
            )}
          </div>

          <Separator />

          {/* Check for updates */}
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <p className="text-sm font-medium">{t("settings.about.checkForUpdates")}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {t("settings.about.checkForUpdatesDesc")}
              </p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={handleCheckUpdates}
              disabled={isCheckingUpdate}
            >
              <RotateCcw className={`h-4 w-4 mr-2 ${isCheckingUpdate ? 'animate-spin' : ''}`} />
              {isCheckingUpdate ? t("settings.about.checking") : t("settings.about.checkUpdates")}
            </Button>
          </div>

          {/* Update info */}
          {updateInfo?.hasUpdate && (
            <>
              <Separator />
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <p className="text-sm font-medium text-green-600">
                    {t("settings.about.newVersionAvailable", { version: updateInfo.latest })}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {t("settings.about.viewReleaseDetails")}
                  </p>
                </div>
                <Button
                  variant="default"
                  size="sm"
                  onClick={() => setShowUpdateModal(true)}
                  className="bg-green-600 hover:bg-green-700"
                >
                  <ExternalLink className="h-4 w-4 mr-2" />
                  {t("settings.about.viewUpdate")}
                </Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* Update Modal */}
      {updateInfo && updateInfo.hasUpdate && (
        <UpdateModal
          open={showUpdateModal}
          onOpenChange={setShowUpdateModal}
          versionInfo={updateInfo}
        />
      )}
    </div>
  )
}