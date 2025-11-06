import { useState, useEffect, useCallback } from 'react';
import versionService, { type VersionInfo } from '../services/versionService';

export interface UseVersionReturn {
  currentVersion: string;
  isLoading: boolean;
  isCheckingUpdate: boolean;
  updateInfo: VersionInfo | null;
  error: string | null;
  checkForUpdates: () => Promise<VersionInfo>;
  forceCheckUpdates: () => Promise<VersionInfo>;
  clearError: () => void;
}

export const useVersion = (): UseVersionReturn => {
  const [currentVersion, setCurrentVersion] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [isCheckingUpdate, setIsCheckingUpdate] = useState(false);
  const [updateInfo, setUpdateInfo] = useState<VersionInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Load current version
  const loadCurrentVersion = useCallback(async () => {
    try {
      setError(null);
      const version = await versionService.getCurrentVersion();
      setCurrentVersion(version.version);
    } catch (err) {
      console.error('Failed to load version:', err);
      setError('Failed to load version information');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Check for updates
  const checkForUpdates = useCallback(async () => {
    try {
      setError(null);
      const updateInfo = await versionService.checkForUpdates();
      setUpdateInfo(updateInfo);
      return updateInfo;
    } catch (err) {
      console.error('Failed to check for updates:', err);
      setError('Failed to check for updates');
      throw err;
    }
  }, []);

  // Force check for updates (bypass cache)
  const forceCheckUpdates = useCallback(async () => {
    setIsCheckingUpdate(true);
    try {
      setError(null);
      const updateInfo = await versionService.forceCheckUpdates();
      setUpdateInfo(updateInfo);
      return updateInfo;
    } catch (err) {
      console.error('Failed to force check for updates:', err);
      setError('Failed to check for updates');
      throw err;
    } finally {
      setIsCheckingUpdate(false);
    }
  }, []);

  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Initialize
  useEffect(() => {
    loadCurrentVersion();
  }, [loadCurrentVersion]);

  // Auto-check for updates on mount (silent check)
  useEffect(() => {
    const autoCheckUpdates = async () => {
      try {
        await checkForUpdates();
      } catch (err) {
        // Silently handle auto-check errors
        console.debug('Auto-check for updates failed:', err);
      }
    };

    if (currentVersion) {
      autoCheckUpdates();
    }
  }, [currentVersion, checkForUpdates]);

  return {
    currentVersion,
    isLoading,
    isCheckingUpdate,
    updateInfo,
    error,
    checkForUpdates,
    forceCheckUpdates,
    clearError,
  };
};