//
//  GradientRevView.m
//  puuten
//
//  Created by wang jialei on 12-10-7.
//
//

#import "GradientRevView.h"
#import "CMGradientLayerRev.h"

@implementation GradientRevView

+(Class)layerClass{
    return [CMGradientLayerRev class];
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
