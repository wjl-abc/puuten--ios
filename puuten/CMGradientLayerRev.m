//
//  CMGradientLayerRev.m
//  puuten
//
//  Created by wang jialei on 12-10-7.
//
//

#import "CMGradientLayerRev.h"

@interface CMGradientLayerRev ()

@end

@implementation CMGradientLayerRev

- (id)init{
	if (self = [super init]) {
		
		UIColor *colorOne	= [UIColor colorWithHue:0.625 saturation:0.0 brightness:0.5 alpha:0.0];
		UIColor *colorTwo	= [UIColor colorWithHue:0.625 saturation:0.0 brightness:0.3 alpha:1.0];
		
		NSArray *colors =  [NSArray arrayWithObjects:(id)colorOne.CGColor, colorTwo.CGColor, nil];
		
		self.colors = colors;
		
		self.endPoint = CGPointMake(0.5, 0.0);
		self.startPoint = CGPointMake(0.5, 1.0);
		
	}
	return self;
}

@end
