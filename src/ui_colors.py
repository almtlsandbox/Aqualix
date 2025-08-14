"""
UI Color Scheme Module
Defines a soft, aquatic-themed color palette for the Aqualix application.
"""

import tkinter as tk

class AqualixColors:
    """
    Soft aquatic color palette for underwater image processing application.
    All colors are carefully chosen to be easy on the eyes while maintaining good contrast.
    """
    
    # === PRIMARY AQUATIC PALETTE ===
    # Deep ocean blue - for main sections
    DEEP_OCEAN = "#2C5F7A"      # Dark blue-teal
    OCEAN_BLUE = "#4A7BA7"      # Medium blue  
    SHALLOW_WATER = "#7FB3D3"   # Light blue
    
    # Coral and warm tones - for buttons and highlights
    CORAL_PINK = "#E8A598"      # Soft coral
    CORAL_ORANGE = "#D2936B"    # Warm coral
    SANDY_BEIGE = "#F4E5D3"     # Light sandy tone
    
    # Seaweed and natural tones - for sections
    SEA_GREEN = "#8DB4A0"       # Soft sea green
    KELP_GREEN = "#6B9080"      # Medium green
    DEEP_SEA_GREEN = "#4A6741"  # Dark green
    
    # === BACKGROUND TONES ===
    # Very soft backgrounds
    PEARL_WHITE = "#F8F9FA"     # Main background
    FOAM_WHITE = "#F0F4F8"      # Panel backgrounds
    MIST_BLUE = "#E8F2F7"       # Light section backgrounds
    SOFT_GRAY = "#E9ECEF"       # Neutral backgrounds
    
    # === ACCENT COLORS ===
    # For special elements
    STARFISH_ORANGE = "#F4A261"  # Warning/attention
    SUNSET_GOLD = "#E9C46A"      # Success/positive
    DEEP_PURPLE = "#7B68EE"      # Info/neutral
    SOFT_LAVENDER = "#DDD6FE"    # Very light accent
    
    # === TEXT COLORS ===
    DEEP_NAVY = "#2D3748"        # Primary text
    MEDIUM_GRAY = "#4A5568"      # Secondary text
    LIGHT_GRAY = "#718096"       # Disabled/placeholder text
    
    # === INTERACTIVE ELEMENTS ===
    # Button states
    BUTTON_PRIMARY = OCEAN_BLUE
    BUTTON_PRIMARY_HOVER = DEEP_OCEAN
    BUTTON_PRIMARY_ACTIVE = "#1A4B66"
    
    BUTTON_SECONDARY = SEA_GREEN
    BUTTON_SECONDARY_HOVER = KELP_GREEN
    BUTTON_SECONDARY_ACTIVE = DEEP_SEA_GREEN
    
    BUTTON_ACCENT = CORAL_ORANGE
    BUTTON_ACCENT_HOVER = "#B8835A"
    BUTTON_ACCENT_ACTIVE = "#A0724D"
    
    # === STATUS COLORS ===
    SUCCESS = "#48BB78"          # Green success
    WARNING = STARFISH_ORANGE    # Orange warning  
    ERROR = "#F56565"            # Red error
    INFO = DEEP_PURPLE           # Purple info
    
    # === SECTION COLORS ===
    # For different parameter sections
    SECTION_WHITE_BALANCE = MIST_BLUE
    SECTION_UDCP = "#FFF0E6"            # Light peach
    SECTION_BEER_LAMBERT = "#E6F7FF"    # Light cyan
    SECTION_COLOR_BALANCE = "#F0F9E8"   # Light mint
    SECTION_HISTOGRAM = "#FDF2E9"       # Light cream
    SECTION_FUSION = "#F3E8FF"          # Light lavender
    
    @classmethod
    def get_section_color(cls, section_name: str) -> str:
        """Get the background color for a specific section"""
        section_colors = {
            'white_balance': cls.SECTION_WHITE_BALANCE,
            'udcp': cls.SECTION_UDCP,
            'beer_lambert': cls.SECTION_BEER_LAMBERT,
            'color_rebalance': cls.SECTION_COLOR_BALANCE,
            'histogram_equalization': cls.SECTION_HISTOGRAM,
            'multiscale_fusion': cls.SECTION_FUSION,
        }
        return section_colors.get(section_name.lower(), cls.FOAM_WHITE)
    
    @classmethod
    def get_button_style(cls, style_type: str = 'primary') -> dict:
        """Get button style configuration"""
        styles = {
            'primary': {
                'bg': cls.BUTTON_PRIMARY,
                'fg': 'white',
                'active_bg': cls.BUTTON_PRIMARY_ACTIVE,
                'hover_bg': cls.BUTTON_PRIMARY_HOVER
            },
            'secondary': {
                'bg': cls.BUTTON_SECONDARY,
                'fg': 'white', 
                'active_bg': cls.BUTTON_SECONDARY_ACTIVE,
                'hover_bg': cls.BUTTON_SECONDARY_HOVER
            },
            'accent': {
                'bg': cls.BUTTON_ACCENT,
                'fg': 'white',
                'active_bg': cls.BUTTON_ACCENT_ACTIVE,
                'hover_bg': cls.BUTTON_ACCENT_HOVER
            }
        }
        return styles.get(style_type, styles['primary'])

class ColoredFrame(tk.Frame):
    """Enhanced Frame with background color support"""
    
    def __init__(self, parent, bg_color=None, **kwargs):
        # Set background color if provided
        if bg_color:
            kwargs['bg'] = bg_color
        elif 'bg' not in kwargs:
            kwargs['bg'] = AqualixColors.FOAM_WHITE
            
        super().__init__(parent, **kwargs)

class SectionFrame(ColoredFrame):
    """Colored frame for parameter sections"""
    
    def __init__(self, parent, section_name=None, **kwargs):
        bg_color = AqualixColors.get_section_color(section_name) if section_name else AqualixColors.FOAM_WHITE
        super().__init__(parent, bg_color=bg_color, **kwargs)
        
        # Add subtle border
        self.configure(relief='solid', bd=1, highlightbackground=AqualixColors.SOFT_GRAY)

class ColoredButton(tk.Button):
    """Enhanced Button with aquatic color styling"""
    
    def __init__(self, parent, style_type='primary', **kwargs):
        style = AqualixColors.get_button_style(style_type)
        
        # Apply style
        kwargs.update({
            'bg': style['bg'],
            'fg': style['fg'],
            'activebackground': style['active_bg'],
            'relief': 'flat',
            'bd': 0,
            'pady': 8,
            'padx': 16,
            'font': ('Arial', 9, 'normal'),
            'cursor': 'hand2'
        })
        
        super().__init__(parent, **kwargs)
        
        # Bind hover effects
        self.bind('<Enter>', lambda e: self.configure(bg=style['hover_bg']))
        self.bind('<Leave>', lambda e: self.configure(bg=style['bg']))
