"""
Interactive component generation
"""
import logging
from typing import Dict, Any, List, Optional
import json
from dataclasses import dataclass, asdict

from ..models.visualization_model import VisualizationModel


logger = logging.getLogger(__name__)


@dataclass
class InteractiveFilter:
    """Interactive filter component"""
    filter_id: str
    filter_type: str  # 'dropdown', 'slider', 'date_range', 'multi_select'
    label: str
    options: List[Any] = None
    default_value: Any = None
    min_value: Any = None
    max_value: Any = None
    step: Any = None


@dataclass
class InteractiveControl:
    """Interactive control component"""
    control_id: str
    control_type: str  # 'button', 'toggle', 'input', 'checkbox'
    label: str
    action: str
    parameters: Dict[str, Any] = None
    style: Dict[str, str] = None


@dataclass
class InteractiveTab:
    """Interactive tab component"""
    tab_id: str
    title: str
    content: Dict[str, Any]
    icon: Optional[str] = None
    active: bool = False


@dataclass
class InteractiveModal:
    """Interactive modal component"""
    modal_id: str
    title: str
    content: Dict[str, Any]
    size: str = 'medium'  # 'small', 'medium', 'large', 'fullscreen'
    trigger: Dict[str, Any] = None


class InteractiveElementsGenerator:
    """Generate interactive components for dashboards and reports"""
    
    def __init__(self):
        self.filter_generators = {
            'dropdown': self._create_dropdown_filter,
            'slider': self._create_slider_filter,
            'date_range': self._create_date_range_filter,
            'multi_select': self._create_multi_select_filter,
            'search': self._create_search_filter
        }
        
        self.control_generators = {
            'button': self._create_button_control,
            'toggle': self._create_toggle_control,
            'input': self._create_input_control,
            'checkbox': self._create_checkbox_control
        }
    
    def create_interactive_dashboard_controls(self, dashboard_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create interactive controls for dashboard"""
        try:
            logger.info("Creating interactive dashboard controls")
            
            controls = {
                'filters': [],
                'navigation': [],
                'export_controls': [],
                'view_controls': []
            }
            
            # Create filters based on data columns
            data_columns = dashboard_config.get('data_columns', [])
            for column in data_columns:
                if column.get('filterable', False):
                    filter_config = self._generate_column_filter(column)
                    if filter_config:
                        controls['filters'].append(filter_config)
            
            # Create navigation controls
            if dashboard_config.get('multi_page', False):
                nav_control = InteractiveControl(
                    control_id='page_navigator',
                    control_type='button',
                    label='Navigate Pages',
                    action='navigate_page',
                    parameters={'pages': dashboard_config.get('pages', [])}
                )
                controls['navigation'].append(asdict(nav_control))
            
            # Create export controls
            export_formats = dashboard_config.get('export_formats', ['png', 'pdf', 'html'])
            for format_type in export_formats:
                export_control = InteractiveControl(
                    control_id=f'export_{format_type}',
                    control_type='button',
                    label=f'Export as {format_type.upper()}',
                    action='export_dashboard',
                    parameters={'format': format_type}
                )
                controls['export_controls'].append(asdict(export_control))
            
            # Create view controls
            view_options = dashboard_config.get('view_options', {})
            if view_options.get('theme_switcher', False):
                theme_control = InteractiveControl(
                    control_id='theme_switcher',
                    control_type='toggle',
                    label='Dark Theme',
                    action='switch_theme',
                    parameters={'themes': ['light', 'dark']}
                )
                controls['view_controls'].append(asdict(theme_control))
            
            if view_options.get('fullscreen', False):
                fullscreen_control = InteractiveControl(
                    control_id='fullscreen_toggle',
                    control_type='button',
                    label='Fullscreen',
                    action='toggle_fullscreen'
                )
                controls['view_controls'].append(asdict(fullscreen_control))
            
            return controls
            
        except Exception as e:
            logger.error(f"Error creating dashboard controls: {e}")
            return {}
    
    def _generate_column_filter(self, column: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate filter for a data column"""
        try:
            column_name = column.get('name', '')
            column_type = column.get('type', 'string')
            
            if column_type in ['string', 'category']:
                return asdict(InteractiveFilter(
                    filter_id=f'filter_{column_name}',
                    filter_type='dropdown',
                    label=f'Filter by {column_name}',
                    options=column.get('unique_values', [])
                ))
            
            elif column_type in ['number', 'integer', 'float']:
                return asdict(InteractiveFilter(
                    filter_id=f'filter_{column_name}',
                    filter_type='slider',
                    label=f'Filter {column_name}',
                    min_value=column.get('min_value', 0),
                    max_value=column.get('max_value', 100),
                    default_value=[column.get('min_value', 0), column.get('max_value', 100)]
                ))
            
            elif column_type in ['date', 'datetime']:
                return asdict(InteractiveFilter(
                    filter_id=f'filter_{column_name}',
                    filter_type='date_range',
                    label=f'Filter {column_name}',
                    min_value=column.get('min_date'),
                    max_value=column.get('max_date')
                ))
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating column filter: {e}")
            return None
    
    def _create_dropdown_filter(self, config: InteractiveFilter) -> Dict[str, Any]:
        """Create dropdown filter component"""
        return {
            'type': 'dropdown',
            'id': config.filter_id,
            'label': config.label,
            'options': [{'label': str(opt), 'value': opt} for opt in (config.options or [])],
            'value': config.default_value,
            'clearable': True,
            'searchable': True
        }
    
    def _create_slider_filter(self, config: InteractiveFilter) -> Dict[str, Any]:
        """Create slider filter component"""
        return {
            'type': 'range_slider',
            'id': config.filter_id,
            'label': config.label,
            'min': config.min_value,
            'max': config.max_value,
            'value': config.default_value or [config.min_value, config.max_value],
            'step': config.step or 1,
            'marks': {
                str(config.min_value): str(config.min_value),
                str(config.max_value): str(config.max_value)
            }
        }
    
    def _create_date_range_filter(self, config: InteractiveFilter) -> Dict[str, Any]:
        """Create date range filter component"""
        return {
            'type': 'date_picker_range',
            'id': config.filter_id,
            'label': config.label,
            'start_date': config.min_value,
            'end_date': config.max_value,
            'display_format': 'YYYY-MM-DD'
        }
    
    def _create_multi_select_filter(self, config: InteractiveFilter) -> Dict[str, Any]:
        """Create multi-select filter component"""
        return {
            'type': 'multi_dropdown',
            'id': config.filter_id,
            'label': config.label,
            'options': [{'label': str(opt), 'value': opt} for opt in (config.options or [])],
            'value': config.default_value or [],
            'clearable': True,
            'searchable': True
        }
    
    def _create_search_filter(self, config: InteractiveFilter) -> Dict[str, Any]:
        """Create search filter component"""
        return {
            'type': 'input',
            'id': config.filter_id,
            'label': config.label,
            'placeholder': f'Search {config.label.lower()}...',
            'type': 'text',
            'debounce': True
        }
    
    def _create_button_control(self, config: InteractiveControl) -> Dict[str, Any]:
        """Create button control component"""
        return {
            'type': 'button',
            'id': config.control_id,
            'children': config.label,
            'n_clicks': 0,
            'style': config.style or {},
            'className': 'interactive-button'
        }
    
    def _create_toggle_control(self, config: InteractiveControl) -> Dict[str, Any]:
        """Create toggle control component"""
        return {
            'type': 'switch',
            'id': config.control_id,
            'label': config.label,
            'value': False,
            'style': config.style or {}
        }
    
    def _create_input_control(self, config: InteractiveControl) -> Dict[str, Any]:
        """Create input control component"""
        return {
            'type': 'input',
            'id': config.control_id,
            'placeholder': config.label,
            'type': 'text',
            'style': config.style or {}
        }
    
    def _create_checkbox_control(self, config: InteractiveControl) -> Dict[str, Any]:
        """Create checkbox control component"""
        return {
            'type': 'checklist',
            'id': config.control_id,
            'options': [{'label': config.label, 'value': config.control_id}],
            'value': [],
            'style': config.style or {}
        }
    
    def create_tabbed_interface(self, tabs: List[InteractiveTab]) -> Dict[str, Any]:
        """Create tabbed interface component"""
        try:
            logger.info(f"Creating tabbed interface with {len(tabs)} tabs")
            
            tab_components = []
            tab_content = []
            
            for tab in tabs:
                # Tab header
                tab_components.append({
                    'label': tab.title,
                    'value': tab.tab_id,
                    'icon': tab.icon
                })
                
                # Tab content
                tab_content.append({
                    'tab_id': tab.tab_id,
                    'content': tab.content
                })
            
            return {
                'type': 'tabs',
                'tabs': tab_components,
                'content': tab_content,
                'active_tab': next((tab.tab_id for tab in tabs if tab.active), tabs[0].tab_id if tabs else None)
            }
            
        except Exception as e:
            logger.error(f"Error creating tabbed interface: {e}")
            return {}
    
    def create_modal_dialog(self, modal: InteractiveModal) -> Dict[str, Any]:
        """Create modal dialog component"""
        try:
            logger.info(f"Creating modal dialog: {modal.title}")
            
            return {
                'type': 'modal',
                'id': modal.modal_id,
                'title': modal.title,
                'content': modal.content,
                'size': modal.size,
                'trigger': modal.trigger,
                'backdrop': True,
                'keyboard_close': True,
                'centered': True
            }
            
        except Exception as e:
            logger.error(f"Error creating modal dialog: {e}")
            return {}
    
    def create_comparison_slider(self, before_content: Dict[str, Any], 
                               after_content: Dict[str, Any]) -> Dict[str, Any]:
        """Create before/after comparison slider"""
        try:
            logger.info("Creating comparison slider")
            
            return {
                'type': 'comparison_slider',
                'id': 'before_after_comparison',
                'before': {
                    'title': 'Before Enhancement',
                    'content': before_content
                },
                'after': {
                    'title': 'After Enhancement',
                    'content': after_content
                },
                'slider_position': 50,  # Default to middle
                'animation': True,
                'labels': True
            }
            
        except Exception as e:
            logger.error(f"Error creating comparison slider: {e}")
            return {}
    
    def create_interactive_timeline(self, timeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create interactive timeline component"""
        try:
            logger.info("Creating interactive timeline")
            
            events = timeline_data.get('events', [])
            processed_events = []
            
            for event in events:
                processed_events.append({
                    'date': event.get('date'),
                    'title': event.get('title'),
                    'description': event.get('description'),
                    'category': event.get('category'),
                    'priority': event.get('priority', 'medium'),
                    'status': event.get('status', 'pending'),
                    'details': event.get('details', {})
                })
            
            return {
                'type': 'timeline',
                'id': 'interactive_timeline',
                'title': timeline_data.get('title', 'Timeline'),
                'events': processed_events,
                'interactive': True,
                'filterable': True,
                'zoomable': True,
                'categories': list(set(event.get('category') for event in events if event.get('category')))
            }
            
        except Exception as e:
            logger.error(f"Error creating interactive timeline: {e}")
            return {}
    
    def create_progress_tracker(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create progress tracking component"""
        try:
            logger.info("Creating progress tracker")
            
            milestones = progress_data.get('milestones', [])
            current_progress = progress_data.get('current_progress', 0)
            
            return {
                'type': 'progress_tracker',
                'id': 'progress_tracker',
                'title': progress_data.get('title', 'Progress'),
                'current_progress': current_progress,
                'total_milestones': len(milestones),
                'milestones': milestones,
                'show_percentage': True,
                'show_details': True,
                'animated': True
            }
            
        except Exception as e:
            logger.error(f"Error creating progress tracker: {e}")
            return {}
    
    def create_notification_system(self, notifications: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create notification system component"""
        try:
            logger.info(f"Creating notification system with {len(notifications)} notifications")
            
            processed_notifications = []
            for notification in notifications:
                processed_notifications.append({
                    'id': notification.get('id'),
                    'type': notification.get('type', 'info'),  # 'success', 'warning', 'error', 'info'
                    'title': notification.get('title'),
                    'message': notification.get('message'),
                    'timestamp': notification.get('timestamp'),
                    'action': notification.get('action'),
                    'dismissible': notification.get('dismissible', True),
                    'auto_dismiss': notification.get('auto_dismiss', False),
                    'duration': notification.get('duration', 5000)
                })
            
            return {
                'type': 'notification_system',
                'id': 'notifications',
                'notifications': processed_notifications,
                'position': 'top-right',
                'max_notifications': 5,
                'stack': True
            }
            
        except Exception as e:
            logger.error(f"Error creating notification system: {e}")
            return {}
    
    def create_interactive_tour(self, tour_steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create interactive tour component"""
        try:
            logger.info(f"Creating interactive tour with {len(tour_steps)} steps")
            
            return {
                'type': 'interactive_tour',
                'id': 'feature_tour',
                'steps': tour_steps,
                'auto_start': False,
                'show_progress': True,
                'show_navigation': True,
                'keyboard_navigation': True,
                'backdrop': True
            }
            
        except Exception as e:
            logger.error(f"Error creating interactive tour: {e}")
            return {}
    
    def generate_responsive_layout(self, components: List[Dict[str, Any]], 
                                 layout_type: str = 'grid') -> Dict[str, Any]:
        """Generate responsive layout for components"""
        try:
            logger.info(f"Creating responsive {layout_type} layout")
            
            if layout_type == 'grid':
                return self._create_grid_layout(components)
            elif layout_type == 'flex':
                return self._create_flex_layout(components)
            elif layout_type == 'masonry':
                return self._create_masonry_layout(components)
            else:
                return self._create_default_layout(components)
            
        except Exception as e:
            logger.error(f"Error generating responsive layout: {e}")
            return {}
    
    def _create_grid_layout(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create CSS Grid layout"""
        return {
            'type': 'grid_layout',
            'components': components,
            'grid_template_columns': 'repeat(auto-fit, minmax(300px, 1fr))',
            'gap': '20px',
            'responsive_breakpoints': {
                'mobile': '(max-width: 768px)',
                'tablet': '(max-width: 1024px)',
                'desktop': '(min-width: 1025px)'
            }
        }
    
    def _create_flex_layout(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create Flexbox layout"""
        return {
            'type': 'flex_layout',
            'components': components,
            'flex_direction': 'row',
            'flex_wrap': 'wrap',
            'justify_content': 'space-between',
            'align_items': 'stretch',
            'gap': '20px'
        }
    
    def _create_masonry_layout(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create Masonry layout"""
        return {
            'type': 'masonry_layout',
            'components': components,
            'columns': 3,
            'gap': '20px',
            'responsive_columns': {
                'mobile': 1,
                'tablet': 2,
                'desktop': 3
            }
        }
    
    def _create_default_layout(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create default stacked layout"""
        return {
            'type': 'stack_layout',
            'components': components,
            'spacing': '20px'
        }
