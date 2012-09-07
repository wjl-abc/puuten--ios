//
//  GradientView.m
//  GradientTest
//
//  Created by wang jialei on 12-9-7.
//  Copyright (c) 2012年 wang jialei. All rights reserved.
//

#import "GradientView.h"
#import "CMGradientLayer.h"

@implementation GradientView

+(Class)layerClass{
    return [CMGradientLayer class];
}

- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        self.backgroundColor = [UIColor clearColor];
        // Initialization code
    }
    return self;
}

/*
// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect
{
    // Drawing code
}
*/


@end
