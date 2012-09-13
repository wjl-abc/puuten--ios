//
//  AFKPageFlipper.h
//  AFKPageFlipper
//
//  Created by Marco Tabini on 10-10-11.
//  Copyright 2010 AFK Studio Partnership. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>


@class AFKPageFlipper;


@protocol AFKPageFlipperDataSource

- (NSInteger) numberOfPagesForPageFlipper:(AFKPageFlipper *) pageFlipper;
- (UIView *) viewForPage:(NSInteger) page inFlipper:(AFKPageFlipper *) pageFlipper;

@end


typedef enum {
	AFKPageFlipperDirectionUp,
	AFKPageFlipperDirectionDown,
} AFKPageFlipperDirection;



@interface AFKPageFlipper : UIView {
	NSObject <AFKPageFlipperDataSource> *dataSource;
	NSInteger currentPage;
	NSInteger numberOfPages;
	
	UIView *currentView;
	UIView *nextView;
	
	CALayer *backgroundAnimationLayer;
	CALayer *flipAnimationLayer;
  
  CALayer *revealedLayer;
  CALayer *coveredLayer;
	
	AFKPageFlipperDirection flipDirection;
	float startFlipAngle;
	float endFlipAngle;
	float currentAngle;

	BOOL setNextViewOnCompletion;
	BOOL animating;
	
	BOOL disabled;
}

@property (nonatomic,retain) NSObject <AFKPageFlipperDataSource> *dataSource;
@property (nonatomic,assign) NSInteger currentPage;

@property (nonatomic, retain) UIPanGestureRecognizer *panRecognizer;

@property (nonatomic,assign) BOOL disabled;

- (void)setCurrentPage:(NSInteger)value animated:(BOOL)animated;

- (void)animateFirstPage;

- (void)setDataSource:(NSObject<AFKPageFlipperDataSource> *)dataSource withPage:(int) page;

@end
