from keystone import *
from capstone import *

keystone_modes = {
        'ARCH_ARM' : {
            'VAL' : KS_ARCH_ARM,
            'MODES' : {
                'MODE_ARM' : {
                    'VAL' : KS_MODE_ARM,
                    'DESCRIPTION' : '32 Bit',
                    'ENDIAN' : {
                        'MODE_LITTLE_ENDIAN': {
                            'VAL': KS_MODE_LITTLE_ENDIAN,
                            'DESCRIPTION' : 'Little Endian'
                            },
                        'MODE_BIG_ENDIAN' : {
                            'VAL': KS_MODE_BIG_ENDIAN,
                            'DESCRIPTION' : 'Big Endian'
                            }
                        }
                    },
                'MODE_THUMB' : {
                    'VAL' : KS_MODE_THUMB,
                    'DESCRIPTION' : '32 Bit Thumb',
                    'ENDIAN' : {
                        'MODE_LITTLE_ENDIAN': {
                            'VAL': KS_MODE_LITTLE_ENDIAN,
                            'DESCRIPTION' : 'Little Endian'
                            },
                        'MODE_BIG_ENDIAN' : {
                            'VAL': KS_MODE_BIG_ENDIAN,
                            'DESCRIPTION' : 'Big Endian'
                            }
                        }
                    }
                }
            },

        'ARCH_ARM64' : {
            'VAL' : KS_ARCH_ARM64,
            'MODES' : {
                'MODE_ARM' : {
                    'VAL' : KS_MODE_LITTLE_ENDIAN,
                    'DESCRIPTION' : '64 Bit',
                    'ENDIAN' : {
                        'MODE_LITTLE_ENDIAN': {
                            'VAL': KS_MODE_LITTLE_ENDIAN,
                            'DESCRIPTION' : 'Little Endian'
                            }
                        }
                    }
                }
            },

        'ARCH_MIPS': {
            'VAL' : KS_ARCH_MIPS,
            'MODES' : {
                'MODE_MIPS32' : {
                    'VAL' : KS_MODE_MIPS32,
                    'DESCRIPTION' : '32 Bit',
                    'ENDIAN' : {
                        'MODE_LITTLE_ENDIAN': {
                            'VAL': KS_MODE_LITTLE_ENDIAN,
                            'DESCRIPTION' : 'Little Endian'
                            },
                        'MODE_BIG_ENDIAN' : {
                            'VAL': KS_MODE_BIG_ENDIAN,
                            'DESCRIPTION' : 'Big Endian'
                            }
                        }
                    },
                'MODE_MIPS64' : {
                    'VAL' : KS_MODE_MIPS64,
                    'DESCRIPTION' : '64 Bit',
                    'ENDIAN' : {
                        'MODE_LITTLE_ENDIAN': {
                            'VAL': KS_MODE_LITTLE_ENDIAN,
                            'DESCRIPTION' : 'Little Endian'
                            },
                        'MODE_BIG_ENDIAN' : {
                            'VAL': KS_MODE_BIG_ENDIAN,
                            'DESCRIPTION' : 'Big Endian'
                            }
                        }
                    }
                }
            },

        'ARCH_SPARC' : {
                'VAL' : KS_ARCH_SPARC,
                'MODES' : {
                    'MODE_SPARC32' : {
                        'VAL' : KS_MODE_SPARC32,
                        'DESCRIPTION' : '32 Bit',
                        'ENDIAN' : {
                            'MODE_LITTLE_ENDIAN': {
                                'VAL': KS_MODE_LITTLE_ENDIAN,
                                'DESCRIPTION' : 'Little Endian'
                                },
                            'MODE_BIG_ENDIAN' : {
                                'VAL': KS_MODE_BIG_ENDIAN,
                                'DESCRIPTION' : 'Big Endian'
                                }
                            }
                        }
                    }
                },

        'ARCH_PPC' : {
                'VAL' : KS_ARCH_PPC,
                'MODES' : {
                    'MODE_PPC32' : {
                        'VAL' : KS_MODE_PPC32,
                        'DESCRIPTION' : '32 Bit',
                        'ENDIAN' : {
                            'MODE_BIG_ENDIAN' : {
                                'VAL': KS_MODE_BIG_ENDIAN,
                                'DESCRIPTION' : 'Big Endian'
                                }
                            }
                        },
                    'MODE_PPC64' : {
                        'VAL' : KS_MODE_PPC64,
                        'DESCRIPTION' : '64 Bit',
                        'ENDIAN' : {
                            'MODE_LITTLE_ENDIAN': {
                                'VAL': KS_MODE_LITTLE_ENDIAN,
                                'DESCRIPTION' : 'Little Endian'
                                },
                            'MODE_BIG_ENDIAN' : {
                                'VAL': KS_MODE_BIG_ENDIAN,
                                'DESCRIPTION' : 'Big Endian'
                                }
                            }
                        }
                    }
                },

        'ARCH_X86' : {
                'VAL' : KS_ARCH_X86,
                'MODES' : {
                    'MODE_64' : {
                        'VAL' : KS_MODE_64,
                        'DESCRIPTION' : '64 Bit',
                        'ENDIAN' : {
                            'MODE_LITTLE_ENDIAN': {
                                'VAL': KS_MODE_LITTLE_ENDIAN,
                                'DESCRIPTION' : 'Little Endian'
                                }
                            }
                        },
                    'MODE_32' : {
                        'VAL' : KS_MODE_32,
                        'DESCRIPTION' : '32 Bit',
                        'ENDIAN' : {
                            'MODE_LITTLE_ENDIAN': {
                                'VAL': KS_MODE_LITTLE_ENDIAN,
                                'DESCRIPTION' : 'Little Endian'
                                }
                            }
                        },
                    'MODE_16' : {
                        'VAL' : KS_MODE_16,
                        'DESCRIPTION' : '16 Bit',
                        'ENDIAN' : {
                            'MODE_LITTLE_ENDIAN': {
                                'VAL': KS_MODE_LITTLE_ENDIAN,
                                'DESCRIPTION' : 'Little Endian'
                                }
                            }
                        }
                    }
                }
        }
