import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Chip,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Tabs,
  Tab,
  Alert,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Switch,
  FormControlLabel
} from '@mui/material';
import {
  Visibility,
  Download,
  Share,
  Print,
  FilterList,
  Search,
  Assessment,
  TrendingUp,
  TrendingDown,
  Timeline,
  PieChart,
  BarChart,
  TableChart,
  InsertChart,
  FileDownload,
  Email,
  Link,
  Refresh
} from '@mui/icons-material';

interface ReportData {
  id: string;
  title: string;
  type: 'analysis' | 'enhancement' | 'modernization' | 'quality' | 'metrics';
  dateGenerated: string;
  author: string;
  summary: string;
  data: any;
  charts: ChartData[];
  tables: TableData[];
  insights: InsightData[];
  recommendations: RecommendationData[];
  metadata: {
    pageCount: number;
    processingTime: number;
    dataPoints: number;
    accuracy: number;
  };
}

interface ChartData {
  id: string;
  title: string;
  type: 'line' | 'bar' | 'pie' | 'scatter' | 'heatmap';
  data: any;
  config: any;
}

interface TableData {
  id: string;
  title: string;
  headers: string[];
  rows: any[][];
  summary?: string;
}

interface InsightData {
  id: string;
  title: string;
  description: string;
  type: 'improvement' | 'issue' | 'trend' | 'recommendation';
  priority: 'high' | 'medium' | 'low';
  metrics?: {
    current: number;
    target: number;
    improvement: number;
  };
}

interface RecommendationData {
  id: string;
  title: string;
  description: string;
  category: string;
  impact: 'high' | 'medium' | 'low';
  effort: 'high' | 'medium' | 'low';
  timeline: string;
  benefits: string[];
}

interface ReportViewerProps {
  reports: ReportData[];
  selectedReport?: ReportData;
  onSelectReport: (report: ReportData) => void;
  onExportReport: (reportId: string, format: 'pdf' | 'excel' | 'html') => void;
  onShareReport: (reportId: string) => void;
  onRefreshData: (reportId: string) => void;
}

const ReportViewer: React.FC<ReportViewerProps> = ({
  reports,
  selectedReport,
  onSelectReport,
  onExportReport,
  onShareReport,
  onRefreshData
}) => {
  const [activeTab, setActiveTab] = useState(0);
  const [filteredReports, setFilteredReports] = useState(reports);
  const [filterType, setFilterType] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [exportDialog, setExportDialog] = useState(false);
  const [selectedExportFormat, setSelectedExportFormat] = useState<'pdf' | 'excel' | 'html'>('pdf');
  const [autoRefresh, setAutoRefresh] = useState(false);

  useEffect(() => {
    let filtered = reports;
    
    if (filterType !== 'all') {
      filtered = filtered.filter(report => report.type === filterType);
    }
    
    if (searchTerm) {
      filtered = filtered.filter(report =>
        report.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.summary.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    setFilteredReports(filtered);
  }, [reports, filterType, searchTerm]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const getReportTypeColor = (type: ReportData['type']) => {
    switch (type) {
      case 'analysis':
        return 'primary';
      case 'enhancement':
        return 'success';
      case 'modernization':
        return 'warning';
      case 'quality':
        return 'error';
      case 'metrics':
        return 'info';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority: 'high' | 'medium' | 'low') => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getImpactIcon = (impact: 'high' | 'medium' | 'low') => {
    switch (impact) {
      case 'high':
        return <TrendingUp color="success" />;
      case 'medium':
        return <Timeline color="warning" />;
      case 'low':
        return <TrendingDown color="error" />;
      default:
        return <Assessment />;
    }
  };

  const openExportDialog = () => {
    setExportDialog(true);
  };

  const closeExportDialog = () => {
    setExportDialog(false);
  };

  const handleExport = () => {
    if (selectedReport) {
      onExportReport(selectedReport.id, selectedExportFormat);
    }
    closeExportDialog();
  };

  const TabPanel: React.FC<{ children: React.ReactNode; value: number; index: number }> = ({
    children,
    value,
    index
  }) => (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );

  const renderCharts = (charts: ChartData[]) => (
    <Grid container spacing={3}>
      {charts.map((chart) => (
        <Grid item xs={12} md={6} key={chart.id}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {chart.title}
              </Typography>
              <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#f5f5f5' }}>
                <Typography variant="body2" color="text.secondary">
                  {chart.type.toUpperCase()} Chart Placeholder
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  const renderTables = (tables: TableData[]) => (
    <Box>
      {tables.map((table) => (
        <Card key={table.id} sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {table.title}
            </Typography>
            {table.summary && (
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {table.summary}
              </Typography>
            )}
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    {table.headers.map((header, index) => (
                      <TableCell key={index}>{header}</TableCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {table.rows.slice(0, 10).map((row, rowIndex) => (
                    <TableRow key={rowIndex}>
                      {row.map((cell, cellIndex) => (
                        <TableCell key={cellIndex}>{cell}</TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            {table.rows.length > 10 && (
              <Typography variant="caption" sx={{ mt: 1, display: 'block' }}>
                Showing 10 of {table.rows.length} rows
              </Typography>
            )}
          </CardContent>
        </Card>
      ))}
    </Box>
  );

  const renderInsights = (insights: InsightData[]) => (
    <Grid container spacing={2}>
      {insights.map((insight) => (
        <Grid item xs={12} md={6} key={insight.id}>
          <Alert 
            severity={insight.type === 'issue' ? 'error' : insight.type === 'improvement' ? 'success' : 'info'}
            sx={{ mb: 2 }}
          >
            <Typography variant="h6">{insight.title}</Typography>
            <Typography variant="body2">{insight.description}</Typography>
            {insight.metrics && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="caption" display="block">
                  Current: {insight.metrics.current} | Target: {insight.metrics.target} | Improvement: +{insight.metrics.improvement}%
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={(insight.metrics.current / insight.metrics.target) * 100}
                  sx={{ mt: 1 }}
                />
              </Box>
            )}
          </Alert>
        </Grid>
      ))}
    </Grid>
  );

  const renderRecommendations = (recommendations: RecommendationData[]) => (
    <Grid container spacing={2}>
      {recommendations.map((rec) => (
        <Grid item xs={12} key={rec.id}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                <Typography variant="h6">{rec.title}</Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Chip label={`${rec.impact} impact`} color={getPriorityColor(rec.impact)} size="small" />
                  <Chip label={`${rec.effort} effort`} variant="outlined" size="small" />
                </Box>
              </Box>
              
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {rec.description}
              </Typography>
              
              <Typography variant="subtitle2" gutterBottom>
                Benefits:
              </Typography>
              <List dense>
                {rec.benefits.map((benefit, index) => (
                  <ListItem key={index} sx={{ py: 0 }}>
                    <ListItemIcon sx={{ minWidth: 20 }}>
                      <TrendingUp fontSize="small" color="success" />
                    </ListItemIcon>
                    <ListItemText primary={benefit} />
                  </ListItem>
                ))}
              </List>
              
              <Typography variant="caption" color="text.secondary">
                Timeline: {rec.timeline}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h4">Report Viewer</Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <FormControlLabel
              control={<Switch checked={autoRefresh} onChange={(e) => setAutoRefresh(e.target.checked)} />}
              label="Auto-refresh"
            />
            <Button
              variant="outlined"
              startIcon={<Refresh />}
              onClick={() => selectedReport && onRefreshData(selectedReport.id)}
              disabled={!selectedReport}
            >
              Refresh
            </Button>
            <Button
              variant="outlined"
              startIcon={<Download />}
              onClick={openExportDialog}
              disabled={!selectedReport}
            >
              Export
            </Button>
            <Button
              variant="outlined"
              startIcon={<Share />}
              onClick={() => selectedReport && onShareReport(selectedReport.id)}
              disabled={!selectedReport}
            >
              Share
            </Button>
          </Box>
        </Box>

        {/* Filters */}
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <TextField
            size="small"
            placeholder="Search reports..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />
            }}
          />
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Filter by type</InputLabel>
            <Select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              label="Filter by type"
            >
              <MenuItem value="all">All Types</MenuItem>
              <MenuItem value="analysis">Analysis</MenuItem>
              <MenuItem value="enhancement">Enhancement</MenuItem>
              <MenuItem value="modernization">Modernization</MenuItem>
              <MenuItem value="quality">Quality</MenuItem>
              <MenuItem value="metrics">Metrics</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Reports List */}
        <Grid item xs={12} md={4}>
          <Typography variant="h6" gutterBottom>
            Available Reports ({filteredReports.length})
          </Typography>
          <Box sx={{ maxHeight: 600, overflow: 'auto' }}>
            {filteredReports.map((report) => (
              <Card
                key={report.id}
                sx={{
                  mb: 2,
                  cursor: 'pointer',
                  border: selectedReport?.id === report.id ? '2px solid' : '1px solid',
                  borderColor: selectedReport?.id === report.id ? 'primary.main' : 'divider'
                }}
                onClick={() => onSelectReport(report)}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                    <Typography variant="h6" noWrap>
                      {report.title}
                    </Typography>
                    <Chip
                      label={report.type}
                      color={getReportTypeColor(report.type)}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {report.summary}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {new Date(report.dateGenerated).toLocaleDateString()} • {report.author}
                  </Typography>
                </CardContent>
              </Card>
            ))}
          </Box>
        </Grid>

        {/* Report Content */}
        <Grid item xs={12} md={8}>
          {selectedReport ? (
            <Box>
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    {selectedReport.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                    {selectedReport.summary}
                  </Typography>
                  
                  <Grid container spacing={2} sx={{ mb: 2 }}>
                    <Grid item xs={6} md={3}>
                      <Typography variant="caption" display="block">Pages</Typography>
                      <Typography variant="h6">{selectedReport.metadata.pageCount}</Typography>
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <Typography variant="caption" display="block">Processing Time</Typography>
                      <Typography variant="h6">{selectedReport.metadata.processingTime}s</Typography>
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <Typography variant="caption" display="block">Data Points</Typography>
                      <Typography variant="h6">{selectedReport.metadata.dataPoints}</Typography>
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <Typography variant="caption" display="block">Accuracy</Typography>
                      <Typography variant="h6">{Math.round(selectedReport.metadata.accuracy * 100)}%</Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
                <Tabs value={activeTab} onChange={handleTabChange}>
                  <Tab label="Overview" icon={<Assessment />} />
                  <Tab label="Charts" icon={<BarChart />} />
                  <Tab label="Tables" icon={<TableChart />} />
                  <Tab label="Insights" icon={<TrendingUp />} />
                  <Tab label="Recommendations" icon={<InsertChart />} />
                </Tabs>
              </Box>

              <TabPanel value={activeTab} index={0}>
                <Typography variant="h6" gutterBottom>Report Overview</Typography>
                <Typography variant="body1">{selectedReport.summary}</Typography>
              </TabPanel>

              <TabPanel value={activeTab} index={1}>
                {renderCharts(selectedReport.charts)}
              </TabPanel>

              <TabPanel value={activeTab} index={2}>
                {renderTables(selectedReport.tables)}
              </TabPanel>

              <TabPanel value={activeTab} index={3}>
                {renderInsights(selectedReport.insights)}
              </TabPanel>

              <TabPanel value={activeTab} index={4}>
                {renderRecommendations(selectedReport.recommendations)}
              </TabPanel>
            </Box>
          ) : (
            <Paper sx={{ p: 4, textAlign: 'center' }}>
              <Typography variant="h6" color="text.secondary">
                Select a report to view its contents
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>

      {/* Export Dialog */}
      <Dialog open={exportDialog} onClose={closeExportDialog}>
        <DialogTitle>Export Report</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>Export Format</InputLabel>
            <Select
              value={selectedExportFormat}
              onChange={(e) => setSelectedExportFormat(e.target.value as 'pdf' | 'excel' | 'html')}
              label="Export Format"
            >
              <MenuItem value="pdf">PDF Document</MenuItem>
              <MenuItem value="excel">Excel Spreadsheet</MenuItem>
              <MenuItem value="html">HTML Report</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeExportDialog}>Cancel</Button>
          <Button onClick={handleExport} variant="contained">
            Export
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ReportViewer;
